from fastapi.testclient import TestClient

from app.documents.chat import get_collect_fields, get_select_document
from app.main import app


def _fake_select_document(messages):
    return "Sounds like a Mutual NDA. Shall we start with that?", "mnda"


def _fake_collect_fields(doc_id, messages, field_values):
    updated = {**field_values, "purpose": "Evaluating a partnership"}
    return "Got it, noted the purpose.", updated


def test_chat_without_doc_id_runs_selection(client: TestClient) -> None:
    app.dependency_overrides[get_select_document] = lambda: _fake_select_document
    try:
        response = client.post(
            "/api/documents/chat",
            json={"messages": [{"role": "user", "content": "I need an NDA"}], "docId": None},
        )
    finally:
        app.dependency_overrides.pop(get_select_document, None)

    assert response.status_code == 200
    body = response.json()
    assert body["docId"] == "mnda"
    assert "<article" in body["html"]


def test_chat_without_doc_id_and_still_unselected_returns_no_html(client: TestClient) -> None:
    app.dependency_overrides[get_select_document] = lambda: (lambda messages: ("Which document do you need?", None))
    try:
        response = client.post(
            "/api/documents/chat",
            json={"messages": [{"role": "user", "content": "I need a contract"}], "docId": None},
        )
    finally:
        app.dependency_overrides.pop(get_select_document, None)

    assert response.status_code == 200
    body = response.json()
    assert body["docId"] is None
    assert body["html"] == ""


def test_chat_with_doc_id_runs_field_collection(client: TestClient) -> None:
    app.dependency_overrides[get_collect_fields] = lambda: _fake_collect_fields
    try:
        response = client.post(
            "/api/documents/chat",
            json={
                "messages": [{"role": "user", "content": "It's for a partnership."}],
                "docId": "mnda",
                "fieldValues": {},
            },
        )
    finally:
        app.dependency_overrides.pop(get_collect_fields, None)

    assert response.status_code == 200
    body = response.json()
    assert body["docId"] == "mnda"
    assert body["fieldValues"]["purpose"] == "Evaluating a partnership"
    assert "Evaluating a partnership" in body["html"]


def test_list_documents_returns_catalog(client: TestClient) -> None:
    response = client.get("/api/documents")
    assert response.status_code == 200
    ids = {doc["id"] for doc in response.json()}
    assert ids == {
        "mnda", "csa", "design-partner", "sla", "psa", "dpa",
        "software-license", "partnership", "pilot", "baa", "ai-addendum",
    }


def test_render_unknown_document_404s(client: TestClient) -> None:
    response = client.post("/api/documents/not-a-doc/render", json={"fieldValues": {}})
    assert response.status_code == 404


def test_render_known_document(client: TestClient) -> None:
    response = client.post(
        "/api/documents/mnda/render",
        json={"fieldValues": {"purpose": "evaluating a merger"}},
    )
    assert response.status_code == 200
    assert "evaluating a merger" in response.json()["html"]


def test_chat_with_unknown_doc_id_404s(client: TestClient) -> None:
    response = client.post(
        "/api/documents/chat",
        json={"messages": [], "docId": "not-a-doc", "fieldValues": {}},
    )
    assert response.status_code == 404
