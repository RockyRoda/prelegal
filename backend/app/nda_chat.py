from fastapi import APIRouter, Depends, HTTPException

from .llm import ChatCompletionFn, get_chat_completion
from .schemas import NDAChatRequest, NDAChatResponse

router = APIRouter(prefix="/api/nda", tags=["nda-chat"])


@router.post("/chat", response_model=NDAChatResponse)
def chat(
    payload: NDAChatRequest,
    chat_fn: ChatCompletionFn = Depends(get_chat_completion),
) -> NDAChatResponse:
    try:
        return chat_fn(payload.messages, payload.ndaData)
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail="The assistant had trouble responding. Please try again.",
        ) from exc
