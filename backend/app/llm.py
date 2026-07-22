"""Builds the NDA chat prompt and calls the LLM via OpenRouter/Cerebras.

The free model this project uses (openai/gpt-oss-20b:free) does not reliably
honor litellm's response_format constraint - it sometimes wraps the JSON in
prose or markdown fences, or skips it entirely. The prompt spells the JSON-only
contract out explicitly, and complete_nda_chat retries once with a firmer
reminder if the first reply doesn't parse.
"""

from collections.abc import Callable

from litellm import completion

from .schemas import ChatMessage, NDAChatResponse, NDAFormData

MODEL = "openrouter/openai/gpt-oss-20b:free"
EXTRA_BODY = {"provider": {"order": ["cerebras"]}}
MAX_ATTEMPTS = 3
MAX_TOKENS = 1024

SYSTEM_PROMPT = """You are a legal-intake assistant helping a user complete the fields
of a Mutual Non-Disclosure Agreement (NDA). Ask about one or two missing or unclear
fields per turn, in plain conversational English. Never invent values the user hasn't
given you. Fields:
- purpose: why the parties are sharing confidential information
- effectiveDate: an ISO date (yyyy-mm-dd) the NDA starts
- mndaTerm / termOfConfidentiality: each has type "expires" (with years: an integer
  number of years) or "perpetual" (years must still be an integer - use 0)
- governingLaw: the US state whose law governs the agreement
- jurisdiction: where courts resolving disputes are located
- modifications: optional free-text changes to the standard terms
- party1 / party2: each has name, title, company, noticeAddress

Always return the COMPLETE ndaData object, every field, every turn - carry forward
every previously known value unchanged unless the user asked to change it. Use an
empty string for any string field still unknown. Assign details to party1 or party2
based on which party the user is currently describing; ask if it's unclear which
party a detail belongs to.

Your entire response must be a single JSON object with exactly two top-level keys,
"reply" (your conversational question or comment, as a string) and "ndaData" (the
complete field object described above). Output nothing before or after the JSON -
no prose, no markdown code fences."""

RETRY_REMINDER = (
    "Your previous reply was not a single valid JSON object with \"reply\" and "
    "\"ndaData\" keys. Respond again with ONLY that JSON object, no other text."
)


def _build_messages(messages: list[ChatMessage], nda_data: NDAFormData) -> list[dict]:
    context = (
        "Current known field values (JSON), to be updated and returned in full:\n"
        f"{nda_data.model_dump_json()}"
    )
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "system", "content": context},
        *[{"role": m.role, "content": m.content} for m in messages],
    ]


def _extract_json_object(content: str | None) -> str:
    """The free model doesn't always honor response_format strictly - it can
    wrap the JSON in prose or markdown code fences, or return no content at
    all. Pull out the outermost {...} block so we still get valid JSON to
    validate; an empty result here fails JSON parsing and triggers a retry.
    """
    if not content:
        return ""
    start = content.find("{")
    end = content.rfind("}")
    if start == -1 or end == -1 or end < start:
        return content
    return content[start : end + 1]


def _call_llm(llm_messages: list[dict]) -> str | None:
    response = completion(
        model=MODEL,
        messages=llm_messages,
        response_format=NDAChatResponse,
        reasoning_effort="low",
        max_tokens=MAX_TOKENS,
        allowed_openai_params=["reasoning_effort"],
        extra_body=EXTRA_BODY,
    )
    return response.choices[0].message.content


def complete_nda_chat(messages: list[ChatMessage], nda_data: NDAFormData) -> NDAChatResponse:
    """Calls the LLM, retrying on both provider errors (rate limits, timeouts)
    and malformed replies, since the free model is unreliable on both fronts.
    """
    llm_messages = _build_messages(messages, nda_data)

    for attempt in range(MAX_ATTEMPTS):
        is_last_attempt = attempt == MAX_ATTEMPTS - 1
        try:
            content = _call_llm(llm_messages)
        except Exception:
            if is_last_attempt:
                raise
            continue

        try:
            return NDAChatResponse.model_validate_json(_extract_json_object(content))
        except ValueError:
            if is_last_attempt:
                raise
            llm_messages = [
                *llm_messages,
                {"role": "assistant", "content": content or ""},
                {"role": "system", "content": RETRY_REMINDER},
            ]

    raise AssertionError("unreachable")


ChatCompletionFn = Callable[[list[ChatMessage], NDAFormData], NDAChatResponse]


def get_chat_completion() -> ChatCompletionFn:
    return complete_nda_chat
