from fastapi import APIRouter, Depends, HTTPException

from .api import DocumentChatRequest, DocumentChatResponse, RenderRequest, RenderResponse
from .chat import CollectFieldsFn, SelectDocumentFn, get_collect_fields, get_select_document
from .registry import DOCUMENTS
from .render import render_document_html

router = APIRouter(prefix="/api/documents", tags=["documents"])


@router.get("")
def list_documents() -> list[dict]:
    return [{"id": s.id, "name": s.name, "description": s.description} for s in DOCUMENTS.values()]


@router.post("/chat", response_model=DocumentChatResponse)
def chat(
    payload: DocumentChatRequest,
    select_document_fn: SelectDocumentFn = Depends(get_select_document),
    collect_fields_fn: CollectFieldsFn = Depends(get_collect_fields),
) -> DocumentChatResponse:
    if payload.docId is not None and payload.docId not in DOCUMENTS:
        raise HTTPException(status_code=404, detail="Unknown document")

    try:
        if payload.docId is None:
            reply, selected_doc_id = select_document_fn(payload.messages)
            html = ""
            if selected_doc_id is not None:
                html = render_document_html(DOCUMENTS[selected_doc_id], payload.fieldValues)
            return DocumentChatResponse(
                reply=reply, docId=selected_doc_id, fieldValues=payload.fieldValues, html=html
            )

        reply, field_values = collect_fields_fn(payload.docId, payload.messages, payload.fieldValues)
        html = render_document_html(DOCUMENTS[payload.docId], field_values)
        return DocumentChatResponse(reply=reply, docId=payload.docId, fieldValues=field_values, html=html)
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail="The assistant had trouble responding. Please try again.",
        ) from exc


@router.post("/{doc_id}/render", response_model=RenderResponse)
def render(doc_id: str, payload: RenderRequest) -> RenderResponse:
    spec = DOCUMENTS.get(doc_id)
    if spec is None:
        raise HTTPException(status_code=404, detail="Unknown document")
    return RenderResponse(html=render_document_html(spec, payload.fieldValues))
