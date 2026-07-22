from app.documents.chat import collect_fields
from app.documents.api import ChatMessage


class _FakeMessage:
    def __init__(self, content: str) -> None:
        self.content = content


class _FakeChoice:
    def __init__(self, content: str) -> None:
        self.message = _FakeMessage(content)


class _FakeResponse:
    def __init__(self, content: str) -> None:
        self.choices = [_FakeChoice(content)]


def test_collect_fields_preserves_prior_value_when_model_omits_it(monkeypatch) -> None:
    # The model forgets to re-mention "purpose" this turn and returns it blank -
    # the previously collected value must survive rather than being wiped out.
    fake_content = '{"reply": "What is the effective date?", "fields": {"purpose": "", "effectiveDate": "2026-08-01"}}'
    monkeypatch.setattr(
        "app.documents.chat.completion", lambda **kwargs: _FakeResponse(fake_content)
    )

    reply, field_values = collect_fields(
        "mnda",
        [ChatMessage(role="user", content="August 1st 2026")],
        {"purpose": "Evaluating a partnership"},
    )

    assert reply == "What is the effective date?"
    assert field_values["purpose"] == "Evaluating a partnership"
    assert field_values["effectiveDate"] == "2026-08-01"
