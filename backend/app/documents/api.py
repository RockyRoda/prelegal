from typing import Literal

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class DocumentChatRequest(BaseModel):
    messages: list[ChatMessage]
    docId: str | None = None
    fieldValues: dict[str, str] = Field(default_factory=dict)


class DocumentChatResponse(BaseModel):
    reply: str
    docId: str | None = None
    fieldValues: dict[str, str] = Field(default_factory=dict)
    html: str = ""


class RenderRequest(BaseModel):
    fieldValues: dict[str, str] = Field(default_factory=dict)


class RenderResponse(BaseModel):
    html: str
