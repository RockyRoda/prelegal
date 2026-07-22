from fastapi.testclient import TestClient


def test_health(client: TestClient) -> None:
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_signup_creates_user_and_returns_token(client: TestClient) -> None:
    response = client.post(
        "/api/auth/signup",
        json={"name": "Ada Lovelace", "email": "ada@example.com", "password": "hunter22"},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["user"]["name"] == "Ada Lovelace"
    assert body["user"]["email"] == "ada@example.com"
    assert isinstance(body["user"]["id"], int)
    assert isinstance(body["token"], str) and body["token"]


def test_signup_duplicate_email_rejected(client: TestClient) -> None:
    client.post(
        "/api/auth/signup",
        json={"name": "Ada Lovelace", "email": "ada@example.com", "password": "hunter22"},
    )
    response = client.post(
        "/api/auth/signup",
        json={"name": "Ada L.", "email": "ada@example.com", "password": "hunter22"},
    )
    assert response.status_code == 409


def test_signup_rejects_short_password(client: TestClient) -> None:
    response = client.post(
        "/api/auth/signup",
        json={"name": "Ada Lovelace", "email": "ada@example.com", "password": "short"},
    )
    assert response.status_code == 422


def test_signin_existing_user(client: TestClient) -> None:
    client.post(
        "/api/auth/signup",
        json={"name": "Ada Lovelace", "email": "ada@example.com", "password": "hunter22"},
    )
    response = client.post(
        "/api/auth/signin", json={"email": "ada@example.com", "password": "hunter22"}
    )
    assert response.status_code == 200
    body = response.json()
    assert body["user"]["name"] == "Ada Lovelace"
    assert isinstance(body["token"], str) and body["token"]


def test_signin_unknown_email_rejected(client: TestClient) -> None:
    response = client.post(
        "/api/auth/signin", json={"email": "nobody@example.com", "password": "hunter22"}
    )
    assert response.status_code == 401


def test_signin_wrong_password_rejected(client: TestClient) -> None:
    client.post(
        "/api/auth/signup",
        json={"name": "Ada Lovelace", "email": "ada@example.com", "password": "hunter22"},
    )
    response = client.post(
        "/api/auth/signin", json={"email": "ada@example.com", "password": "wrong-password"}
    )
    assert response.status_code == 401


def test_signin_is_case_insensitive(client: TestClient) -> None:
    client.post(
        "/api/auth/signup",
        json={"name": "Ada Lovelace", "email": "Ada@Example.com", "password": "hunter22"},
    )
    response = client.post(
        "/api/auth/signin", json={"email": "ada@example.com", "password": "hunter22"}
    )
    assert response.status_code == 200
    assert response.json()["user"]["email"] == "ada@example.com"


def test_signup_duplicate_email_rejected_regardless_of_case(client: TestClient) -> None:
    client.post(
        "/api/auth/signup",
        json={"name": "Ada Lovelace", "email": "ada@example.com", "password": "hunter22"},
    )
    response = client.post(
        "/api/auth/signup",
        json={"name": "Ada L.", "email": "Ada@Example.com", "password": "hunter22"},
    )
    assert response.status_code == 409


def test_signin_issues_a_new_token_each_time(client: TestClient) -> None:
    client.post(
        "/api/auth/signup",
        json={"name": "Ada Lovelace", "email": "ada@example.com", "password": "hunter22"},
    )
    first = client.post(
        "/api/auth/signin", json={"email": "ada@example.com", "password": "hunter22"}
    )
    second = client.post(
        "/api/auth/signin", json={"email": "ada@example.com", "password": "hunter22"}
    )
    assert first.json()["token"] != second.json()["token"]
