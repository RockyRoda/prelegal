from fastapi.testclient import TestClient


def test_health(client: TestClient) -> None:
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_signup_creates_user(client: TestClient) -> None:
    response = client.post(
        "/api/auth/signup", json={"name": "Ada Lovelace", "email": "ada@example.com"}
    )
    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "Ada Lovelace"
    assert body["email"] == "ada@example.com"
    assert isinstance(body["id"], int)


def test_signup_duplicate_email_rejected(client: TestClient) -> None:
    client.post("/api/auth/signup", json={"name": "Ada Lovelace", "email": "ada@example.com"})
    response = client.post(
        "/api/auth/signup", json={"name": "Ada L.", "email": "ada@example.com"}
    )
    assert response.status_code == 409


def test_signin_existing_user(client: TestClient) -> None:
    client.post("/api/auth/signup", json={"name": "Ada Lovelace", "email": "ada@example.com"})
    response = client.post("/api/auth/signin", json={"email": "ada@example.com"})
    assert response.status_code == 200
    assert response.json()["name"] == "Ada Lovelace"


def test_signin_unknown_email_rejected(client: TestClient) -> None:
    response = client.post("/api/auth/signin", json={"email": "nobody@example.com"})
    assert response.status_code == 404


def test_signin_is_case_insensitive(client: TestClient) -> None:
    client.post("/api/auth/signup", json={"name": "Ada Lovelace", "email": "Ada@Example.com"})
    response = client.post("/api/auth/signin", json={"email": "ada@example.com"})
    assert response.status_code == 200
    assert response.json()["email"] == "ada@example.com"


def test_signup_duplicate_email_rejected_regardless_of_case(client: TestClient) -> None:
    client.post("/api/auth/signup", json={"name": "Ada Lovelace", "email": "ada@example.com"})
    response = client.post(
        "/api/auth/signup", json={"name": "Ada L.", "email": "Ada@Example.com"}
    )
    assert response.status_code == 409
