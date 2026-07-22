"""Per-user persistence for in-progress and completed documents."""

import json
import sqlite3


def create_document(
    db: sqlite3.Connection, user_id: int, catalog_doc_id: str, field_values: dict[str, str]
) -> int:
    cursor = db.execute(
        "INSERT INTO documents (user_id, catalog_doc_id, field_values) VALUES (?, ?, ?)",
        (user_id, catalog_doc_id, json.dumps(field_values)),
    )
    db.commit()
    return cursor.lastrowid


def update_document(
    db: sqlite3.Connection, document_id: int, user_id: int, field_values: dict[str, str]
) -> None:
    db.execute(
        "UPDATE documents SET field_values = ?, updated_at = CURRENT_TIMESTAMP "
        "WHERE id = ? AND user_id = ?",
        (json.dumps(field_values), document_id, user_id),
    )
    db.commit()


def get_document(db: sqlite3.Connection, document_id: int, user_id: int) -> sqlite3.Row | None:
    return db.execute(
        "SELECT id, catalog_doc_id, field_values, updated_at FROM documents "
        "WHERE id = ? AND user_id = ?",
        (document_id, user_id),
    ).fetchone()


def list_documents(db: sqlite3.Connection, user_id: int) -> list[sqlite3.Row]:
    return db.execute(
        "SELECT id, catalog_doc_id, field_values, updated_at FROM documents "
        "WHERE user_id = ? ORDER BY updated_at DESC",
        (user_id,),
    ).fetchall()
