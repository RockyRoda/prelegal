import sqlite3

from fastapi import APIRouter, Depends, HTTPException

from .db import get_db
from .schemas import SigninRequest, SignupRequest, UserResponse

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/signup", response_model=UserResponse, status_code=201)
def signup(payload: SignupRequest, db: sqlite3.Connection = Depends(get_db)) -> UserResponse:
    existing = db.execute("SELECT id FROM users WHERE email = ?", (payload.email,)).fetchone()
    if existing is not None:
        raise HTTPException(status_code=409, detail="Email already registered")

    cursor = db.execute(
        "INSERT INTO users (name, email) VALUES (?, ?)",
        (payload.name, payload.email),
    )
    db.commit()
    return UserResponse(id=cursor.lastrowid, name=payload.name, email=payload.email)


@router.post("/signin", response_model=UserResponse)
def signin(payload: SigninRequest, db: sqlite3.Connection = Depends(get_db)) -> UserResponse:
    row = db.execute(
        "SELECT id, name, email FROM users WHERE email = ?", (payload.email,)
    ).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="No account found for this email")
    return UserResponse(id=row["id"], name=row["name"], email=row["email"])
