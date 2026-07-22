from pydantic import BaseModel, EmailStr, Field, field_validator


class _LowercaseEmail:
    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        return value.lower()


class SignupRequest(_LowercaseEmail, BaseModel):
    name: str
    email: EmailStr
    password: str = Field(min_length=8)


class SigninRequest(_LowercaseEmail, BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str


class AuthResponse(BaseModel):
    user: UserResponse
    token: str
