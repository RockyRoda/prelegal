import secrets
import sqlite3

import bcrypt
from fastapi import APIRouter, Depends, Header, HTTPException

from .db import get_db
from .schemas import AuthResponse, SigninRequest, SignupRequest, UserResponse

router = APIRouter(prefix="/api/auth", tags=["auth"])


def _create_session(db: sqlite3.Connection, user_id: int) -> str:
    token = secrets.token_urlsafe(32)
    db.execute("INSERT INTO sessions (token, user_id) VALUES (?, ?)", (token, user_id))
    db.commit()
    return token


def get_current_user_id(
    authorization: str | None = Header(default=None),
    db: sqlite3.Connection = Depends(get_db),
) -> int:
    token = (authorization or "").removeprefix("Bearer ").strip()
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    row = db.execute("SELECT user_id FROM sessions WHERE token = ?", (token,)).fetchone()
    if row is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return row["user_id"]


@router.post("/signup", response_model=AuthResponse, status_code=201)
def signup(payload: SignupRequest, db: sqlite3.Connection = Depends(get_db)) -> AuthResponse:
    existing = db.execute("SELECT id FROM users WHERE email = ?", (payload.email,)).fetchone()
    if existing is not None:
        raise HTTPException(status_code=409, detail="Email already registered")

    password_hash = bcrypt.hashpw(payload.password.encode(), bcrypt.gensalt()).decode()
    cursor = db.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        (payload.name, payload.email, password_hash),
    )
    db.commit()
    user = UserResponse(id=cursor.lastrowid, name=payload.name, email=payload.email)
    return AuthResponse(user=user, token=_create_session(db, user.id))


@router.post("/signin", response_model=AuthResponse)
def signin(payload: SigninRequest, db: sqlite3.Connection = Depends(get_db)) -> AuthResponse:
    row = db.execute(
        "SELECT id, name, email, password_hash FROM users WHERE email = ?", (payload.email,)
    ).fetchone()
    if row is None or not bcrypt.checkpw(payload.password.encode(), row["password_hash"].encode()):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    user = UserResponse(id=row["id"], name=row["name"], email=row["email"])
    return AuthResponse(user=user, token=_create_session(db, user.id))
