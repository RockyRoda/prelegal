from typing import Literal

from pydantic import BaseModel, EmailStr, field_validator


class _LowercaseEmail:
    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        return value.lower()


class SignupRequest(_LowercaseEmail, BaseModel):
    name: str
    email: EmailStr


class SigninRequest(_LowercaseEmail, BaseModel):
    email: EmailStr


class UserResponse(BaseModel):
    id: int
    name: str
    email: str


class TermChoice(BaseModel):
    type: Literal["expires", "perpetual"]
    years: int


class PartyDetails(BaseModel):
    name: str
    title: str
    company: str
    noticeAddress: str


class NDAFormData(BaseModel):
    purpose: str
    effectiveDate: str
    mndaTerm: TermChoice
    termOfConfidentiality: TermChoice
    governingLaw: str
    jurisdiction: str
    modifications: str
    party1: PartyDetails
    party2: PartyDetails


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class NDAChatRequest(BaseModel):
    messages: list[ChatMessage]
    ndaData: NDAFormData


class NDAChatResponse(BaseModel):
    reply: str
    ndaData: NDAFormData
