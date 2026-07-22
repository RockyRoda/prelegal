from fastapi.testclient import TestClient

from app.documents.chat import get_collect_fields, get_select_document
from app.main import app


def _fake_select_document(messages):
    return "Sounds like a Mutual NDA. Shall we start with that?", "mnda"


def _fake_collect_fields(doc_id, messages, field_values):
    updated = {**field_values, "purpose": "Evaluating a partnership"}
    return "Got it, noted the purpose.", updated


def test_chat_without_auth_is_rejected(client: TestClient) -> None:
    response = client.post(
        "/api/documents/chat",
        json={"messages": [{"role": "user", "content": "I need an NDA"}], "docId": None},
    )
    assert response.status_code == 401


def test_chat_without_doc_id_runs_selection(client: TestClient, auth_headers: dict[str, str]) -> None:
    app.dependency_overrides[get_select_document] = lambda: _fake_select_document
    try:
        response = client.post(
            "/api/documents/chat",
            json={"messages": [{"role": "user", "content": "I need an NDA"}], "docId": None},
            headers=auth_headers,
        )
    finally:
        app.dependency_overrides.pop(get_select_document, None)

    assert response.status_code == 200
    body = response.json()
    assert body["docId"] == "mnda"
    assert isinstance(body["documentId"], int)
    assert "<article" in body["html"]


def test_chat_without_doc_id_and_still_unselected_returns_no_html(
    client: TestClient, auth_headers: dict[str, str]
) -> None:
    app.dependency_overrides[get_select_document] = lambda: (lambda messages: ("Which document do you need?", None))
    try:
        response = client.post(
            "/api/documents/chat",
            json={"messages": [{"role": "user", "content": "I need a contract"}], "docId": None},
            headers=auth_headers,
        )
    finally:
        app.dependency_overrides.pop(get_select_document, None)

    assert response.status_code == 200
    body = response.json()
    assert body["docId"] is None
    assert body["documentId"] is None
    assert body["html"] == ""


def test_chat_with_doc_id_runs_field_collection_and_creates_a_document(
    client: TestClient, auth_headers: dict[str, str]
) -> None:
    app.dependency_overrides[get_collect_fields] = lambda: _fake_collect_fields
    try:
        response = client.post(
            "/api/documents/chat",
            json={
                "messages": [{"role": "user", "content": "It's for a partnership."}],
                "docId": "mnda",
                "documentId": None,
                "fieldValues": {},
            },
            headers=auth_headers,
        )
    finally:
        app.dependency_overrides.pop(get_collect_fields, None)

    assert response.status_code == 200
    body = response.json()
    assert body["docId"] == "mnda"
    assert isinstance(body["documentId"], int)
    assert body["fieldValues"]["purpose"] == "Evaluating a partnership"
    assert "Evaluating a partnership" in body["html"]


def test_chat_with_existing_document_id_updates_it_in_place(
    client: TestClient, auth_headers: dict[str, str]
) -> None:
    app.dependency_overrides[get_collect_fields] = lambda: _fake_collect_fields
    try:
        first = client.post(
            "/api/documents/chat",
            json={"messages": [], "docId": "mnda", "documentId": None, "fieldValues": {}},
            headers=auth_headers,
        )
        document_id = first.json()["documentId"]

        second = client.post(
            "/api/documents/chat",
            json={"messages": [], "docId": "mnda", "documentId": document_id, "fieldValues": {}},
            headers=auth_headers,
        )
    finally:
        app.dependency_overrides.pop(get_collect_fields, None)

    assert second.json()["documentId"] == document_id

    history = client.get("/api/documents/history", headers=auth_headers)
    assert len(history.json()["documents"]) == 1


def test_history_lists_only_the_current_users_documents(client: TestClient) -> None:
    app.dependency_overrides[get_collect_fields] = lambda: _fake_collect_fields
    try:
        alice = client.post(
            "/api/auth/signup",
            json={"name": "Alice", "email": "alice@example.com", "password": "hunter22"},
        ).json()
        bob = client.post(
            "/api/auth/signup",
            json={"name": "Bob", "email": "bob@example.com", "password": "hunter22"},
        ).json()
        alice_headers = {"Authorization": f"Bearer {alice['token']}"}
        bob_headers = {"Authorization": f"Bearer {bob['token']}"}

        client.post(
            "/api/documents/chat",
            json={"messages": [], "docId": "mnda", "documentId": None, "fieldValues": {}},
            headers=alice_headers,
        )

        alice_history = client.get("/api/documents/history", headers=alice_headers)
        bob_history = client.get("/api/documents/history", headers=bob_headers)
    finally:
        app.dependency_overrides.pop(get_collect_fields, None)

    assert len(alice_history.json()["documents"]) == 1
    assert alice_history.json()["documents"][0]["docId"] == "mnda"
    assert bob_history.json()["documents"] == []


def test_history_detail_resumes_a_document(client: TestClient, auth_headers: dict[str, str]) -> None:
    app.dependency_overrides[get_collect_fields] = lambda: _fake_collect_fields
    try:
        created = client.post(
            "/api/documents/chat",
            json={"messages": [], "docId": "mnda", "documentId": None, "fieldValues": {}},
            headers=auth_headers,
        )
    finally:
        app.dependency_overrides.pop(get_collect_fields, None)
    document_id = created.json()["documentId"]

    response = client.get(f"/api/documents/history/{document_id}", headers=auth_headers)
    assert response.status_code == 200
    body = response.json()
    assert body["docId"] == "mnda"
    assert body["fieldValues"]["purpose"] == "Evaluating a partnership"
    assert "Evaluating a partnership" in body["html"]


def test_history_detail_404s_for_another_users_document(client: TestClient) -> None:
    app.dependency_overrides[get_collect_fields] = lambda: _fake_collect_fields
    try:
        alice = client.post(
            "/api/auth/signup",
            json={"name": "Alice", "email": "alice@example.com", "password": "hunter22"},
        ).json()
        bob = client.post(
            "/api/auth/signup",
            json={"name": "Bob", "email": "bob@example.com", "password": "hunter22"},
        ).json()
        alice_headers = {"Authorization": f"Bearer {alice['token']}"}
        bob_headers = {"Authorization": f"Bearer {bob['token']}"}

        created = client.post(
            "/api/documents/chat",
            json={"messages": [], "docId": "mnda", "documentId": None, "fieldValues": {}},
            headers=alice_headers,
        )
        document_id = created.json()["documentId"]

        response = client.get(f"/api/documents/history/{document_id}", headers=bob_headers)
    finally:
        app.dependency_overrides.pop(get_collect_fields, None)

    assert response.status_code == 404


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


def test_chat_with_unknown_doc_id_404s(client: TestClient, auth_headers: dict[str, str]) -> None:
    response = client.post(
        "/api/documents/chat",
        json={"messages": [], "docId": "not-a-doc", "fieldValues": {}},
        headers=auth_headers,
    )
    assert response.status_code == 404
