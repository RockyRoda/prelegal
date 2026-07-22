"""Builds chat prompts and calls the LLM via OpenRouter/Cerebras.

Two modes share the same retry/JSON-extraction machinery, needed because the
LLM doesn't always honor response_format strictly (see PL-5): document
selection uses a small fixed schema to figure out which catalog document the
user wants; once one is chosen, field collection uses a schema built at
runtime from that document's FieldSpecs, so we don't hand-write 11 separate
Pydantic response models.
"""

from collections.abc import Callable
from typing import Literal

from litellm import completion
from pydantic import BaseModel, ConfigDict, Field, create_model

from .api import ChatMessage
from .registry import DOCUMENTS
from .schema import DocumentSpec, FieldKind, FieldSpec

MODEL = "openrouter/openai/gpt-oss-120b"
EXTRA_BODY = {"provider": {"order": ["cerebras"]}}
MAX_ATTEMPTS = 3
MAX_TOKENS = 1536

RETRY_REMINDER = (
    "Your previous reply was not a single valid JSON object matching the "
    "required schema. Respond again with ONLY that JSON object, no other text."
)

_CATALOG_LISTING = "\n".join(
    f"- {spec.id}: {spec.name} - {spec.description}" for spec in DOCUMENTS.values()
)

# Literal[some_tuple] unpacks into a Literal of every catalog doc id, built at
# import time so the model can only ever select a real, known document.
SelectableDocId = Literal[tuple(DOCUMENTS.keys())]


class SelectionResponse(BaseModel):
    reply: str
    selectedDocId: SelectableDocId | None = None


SELECTION_SYSTEM_PROMPT = f"""You help a user pick which legal document to create. We can only generate these documents:
{_CATALOG_LISTING}

Ask the user what they need if it's unclear. If they describe something not in the list above, explain we can't generate that exact document, but suggest the closest match from the list and ask if that works instead. Once you and the user agree on one specific document from the list, set selectedDocId to its id exactly as shown above (e.g. "mnda"). Otherwise leave selectedDocId null and keep the conversation going.

Your entire response must be a single JSON object with exactly two keys, "reply" and "selectedDocId". Output nothing before or after the JSON - no prose, no markdown code fences."""


def _field_type(field: FieldSpec) -> type:
    if field.kind == FieldKind.ENUM and field.options:
        # "" is the sentinel for "not yet known", same convention as string fields.
        return Literal[(*field.options, "")]
    return str


def _field_description(field: FieldSpec) -> str:
    description = field.help_text or field.label
    if field.kind == FieldKind.ENUM and field.options:
        description += f" (must be exactly one of: {', '.join(field.options)}, or empty if unknown)"
    return description


def _build_field_model(spec: DocumentSpec) -> type[BaseModel]:
    field_definitions = {
        field.name: (
            _field_type(field),
            Field(default="", description=_field_description(field)),
        )
        for field in spec.fields
    }
    return create_model(
        f"Fields_{spec.id}",
        __config__=ConfigDict(extra="ignore"),
        **field_definitions,
    )


def _build_chat_response_model(spec: DocumentSpec) -> type[BaseModel]:
    fields_model = _build_field_model(spec)
    return create_model(
        f"ChatResponse_{spec.id}",
        reply=(str, ...),
        fields=(fields_model, ...),
    )


def _field_collection_system_prompt(spec: DocumentSpec) -> str:
    field_lines = "\n".join(
        f"- {field.name} ({field.label}){'' if field.required else ' [optional]'}"
        + (f": {field.help_text}" if field.help_text else "")
        for field in spec.fields
    )
    return f"""You are a legal-intake assistant helping a user complete the fields of a {spec.name}. Ask about one or two missing or unclear fields per turn, in plain conversational English. Never invent values the user hasn't given you. Fields:
{field_lines}

Always return the COMPLETE set of fields, every turn - carry forward every previously known value unchanged unless the user asked to change it. Use an empty string for any field still unknown.

Your entire response must be a single JSON object with exactly two top-level keys, "reply" and "fields" (an object with every field name above as a key). Output nothing before or after the JSON - no prose, no markdown code fences."""


def _extract_json_object(content: str | None) -> str:
    if not content:
        return ""
    start = content.find("{")
    end = content.rfind("}")
    if start == -1 or end == -1 or end < start:
        return content
    return content[start : end + 1]


def _call_llm(llm_messages: list[dict], response_model: type[BaseModel]) -> str | None:
    response = completion(
        model=MODEL,
        messages=llm_messages,
        response_format=response_model,
        reasoning_effort="low",
        max_tokens=MAX_TOKENS,
        allowed_openai_params=["reasoning_effort"],
        extra_body=EXTRA_BODY,
    )
    return response.choices[0].message.content


def _complete(llm_messages: list[dict], response_model: type[BaseModel]) -> BaseModel:
    messages = llm_messages
    for attempt in range(MAX_ATTEMPTS):
        is_last_attempt = attempt == MAX_ATTEMPTS - 1
        try:
            content = _call_llm(messages, response_model)
        except Exception:
            if is_last_attempt:
                raise
            continue

        try:
            return response_model.model_validate_json(_extract_json_object(content))
        except ValueError:
            if is_last_attempt:
                raise
            messages = [
                *messages,
                {"role": "assistant", "content": content or ""},
                {"role": "system", "content": RETRY_REMINDER},
            ]

    raise AssertionError("unreachable")


def select_document(messages: list[ChatMessage]) -> tuple[str, str | None]:
    llm_messages = [
        {"role": "system", "content": SELECTION_SYSTEM_PROMPT},
        *[{"role": m.role, "content": m.content} for m in messages],
    ]
    result = _complete(llm_messages, SelectionResponse)
    return result.reply, result.selectedDocId


def collect_fields(
    doc_id: str, messages: list[ChatMessage], field_values: dict[str, str]
) -> tuple[str, dict[str, str]]:
    spec = DOCUMENTS[doc_id]
    response_model = _build_chat_response_model(spec)
    state_note = (
        "Current field values (JSON), to be updated and returned in full:\n"
        f"{spec.id}: {field_values}"
    )
    llm_messages = [
        {"role": "system", "content": _field_collection_system_prompt(spec)},
        {"role": "system", "content": state_note},
        *[{"role": m.role, "content": m.content} for m in messages],
    ]
    result = _complete(llm_messages, response_model)
    # The model is asked to return the complete field set every turn, but
    # smaller models sometimes drop a field it forgot to mention rather than
    # carrying it forward - only apply values it actually provided, so a
    # previously-collected answer never silently reverts to blank.
    new_values = {name: value for name, value in result.fields.model_dump().items() if value}
    return result.reply, {**field_values, **new_values}


SelectDocumentFn = Callable[[list[ChatMessage]], tuple[str, str | None]]
CollectFieldsFn = Callable[[str, list[ChatMessage], dict[str, str]], tuple[str, dict[str, str]]]


def get_select_document() -> SelectDocumentFn:
    return select_document


def get_collect_fields() -> CollectFieldsFn:
    return collect_fields
