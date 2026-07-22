import json
import sqlite3

from fastapi import APIRouter, Depends, HTTPException

from ..auth import get_current_user_id
from ..db import get_db
from .api import (
    DocumentChatRequest,
    DocumentChatResponse,
    DocumentDetailResponse,
    DocumentHistoryItem,
    DocumentHistoryResponse,
    RenderRequest,
    RenderResponse,
)
from .chat import CollectFieldsFn, SelectDocumentFn, get_collect_fields, get_select_document
from .registry import DOCUMENTS
from .render import render_document_html
from .store import create_document, get_document, list_documents, update_document

router = APIRouter(prefix="/api/documents", tags=["documents"])


@router.get("")
def list_documents_catalog() -> list[dict]:
    return [{"id": s.id, "name": s.name, "description": s.description} for s in DOCUMENTS.values()]


@router.post("/chat", response_model=DocumentChatResponse)
def chat(
    payload: DocumentChatRequest,
    user_id: int = Depends(get_current_user_id),
    db: sqlite3.Connection = Depends(get_db),
    select_document_fn: SelectDocumentFn = Depends(get_select_document),
    collect_fields_fn: CollectFieldsFn = Depends(get_collect_fields),
) -> DocumentChatResponse:
    if payload.docId is not None and payload.docId not in DOCUMENTS:
        raise HTTPException(status_code=404, detail="Unknown document")

    try:
        if payload.docId is None:
            reply, selected_doc_id = select_document_fn(payload.messages)
            html = ""
            document_id = payload.documentId
            if selected_doc_id is not None:
                html = render_document_html(DOCUMENTS[selected_doc_id], payload.fieldValues)
                document_id = create_document(db, user_id, selected_doc_id, payload.fieldValues)
            return DocumentChatResponse(
                reply=reply,
                docId=selected_doc_id,
                documentId=document_id,
                fieldValues=payload.fieldValues,
                html=html,
            )

        reply, field_values = collect_fields_fn(payload.docId, payload.messages, payload.fieldValues)
        html = render_document_html(DOCUMENTS[payload.docId], field_values)
        if payload.documentId is not None:
            update_document(db, payload.documentId, user_id, field_values)
            document_id = payload.documentId
        else:
            document_id = create_document(db, user_id, payload.docId, field_values)
        return DocumentChatResponse(
            reply=reply, docId=payload.docId, documentId=document_id, fieldValues=field_values, html=html
        )
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail="The assistant had trouble responding. Please try again.",
        ) from exc


@router.get("/history", response_model=DocumentHistoryResponse)
def history(
    user_id: int = Depends(get_current_user_id),
    db: sqlite3.Connection = Depends(get_db),
) -> DocumentHistoryResponse:
    rows = list_documents(db, user_id)
    return DocumentHistoryResponse(
        documents=[
            DocumentHistoryItem(
                documentId=row["id"],
                docId=row["catalog_doc_id"],
                docName=DOCUMENTS[row["catalog_doc_id"]].name,
                updatedAt=row["updated_at"],
            )
            for row in rows
        ]
    )


@router.get("/history/{document_id}", response_model=DocumentDetailResponse)
def history_detail(
    document_id: int,
    user_id: int = Depends(get_current_user_id),
    db: sqlite3.Connection = Depends(get_db),
) -> DocumentDetailResponse:
    row = get_document(db, document_id, user_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Document not found")

    field_values = json.loads(row["field_values"])
    html = render_document_html(DOCUMENTS[row["catalog_doc_id"]], field_values)
    return DocumentDetailResponse(
        documentId=row["id"], docId=row["catalog_doc_id"], fieldValues=field_values, html=html
    )


@router.post("/{doc_id}/render", response_model=RenderResponse)
def render(doc_id: str, payload: RenderRequest) -> RenderResponse:
    spec = DOCUMENTS.get(doc_id)
    if spec is None:
        raise HTTPException(status_code=404, detail="Unknown document")
    return RenderResponse(html=render_document_html(spec, payload.fieldValues))
