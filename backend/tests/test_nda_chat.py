from fastapi.testclient import TestClient

from app.llm import get_chat_completion
from app.main import app
from app.schemas import NDAChatResponse, NDAFormData, PartyDetails, TermChoice


def _empty_nda_data() -> NDAFormData:
    party = PartyDetails(name="", title="", company="", noticeAddress="")
    term = TermChoice(type="expires", years=1)
    return NDAFormData(
        purpose="",
        effectiveDate="",
        mndaTerm=term,
        termOfConfidentiality=term,
        governingLaw="",
        jurisdiction="",
        modifications="",
        party1=party,
        party2=party,
    )


def _stub_chat_completion(messages, nda_data):
    updated = nda_data.model_copy(update={"purpose": "Evaluating a partnership"})
    return NDAChatResponse(reply="Got it, noted the purpose.", ndaData=updated)


def test_chat_returns_reply_and_full_nda_data(client: TestClient) -> None:
    app.dependency_overrides[get_chat_completion] = lambda: _stub_chat_completion
    try:
        response = client.post(
            "/api/nda/chat",
            json={
                "messages": [{"role": "user", "content": "It's for a partnership."}],
                "ndaData": _empty_nda_data().model_dump(),
            },
        )
    finally:
        del app.dependency_overrides[get_chat_completion]

    assert response.status_code == 200
    body = response.json()
    assert body["reply"] == "Got it, noted the purpose."
    assert body["ndaData"]["purpose"] == "Evaluating a partnership"


def test_chat_rejects_malformed_nda_data(client: TestClient) -> None:
    response = client.post(
        "/api/nda/chat",
        json={"messages": [], "ndaData": {"purpose": "x"}},
    )
    assert response.status_code == 422
