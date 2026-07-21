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
