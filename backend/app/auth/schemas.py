from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, BeforeValidator, ConfigDict, EmailStr, Field, field_validator

from app.core.security import password_policy_error


def _norm_email(v: object) -> object:
    return v.strip().lower() if isinstance(v, str) else v


NormalizedEmail = Annotated[EmailStr, BeforeValidator(_norm_email), Field(max_length=254)]


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    email: str
    role: str


class RegisterIn(BaseModel):
    model_config = ConfigDict(extra="forbid")  # `role` u otros campos nunca se aceptan
    email: NormalizedEmail
    password: str

    @field_validator("password")
    @classmethod
    def _policy(cls, v: str) -> str:
        err = password_policy_error(v)
        if err:
            raise ValueError(err)
        return v


class LoginIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    email: Annotated[str, BeforeValidator(_norm_email), Field(min_length=1, max_length=254)]
    password: Annotated[str, Field(min_length=1, max_length=128)]


class ForgotIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    email: Annotated[str, BeforeValidator(_norm_email), Field(min_length=1, max_length=254)]


class ResetIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    token: Annotated[str, Field(min_length=1, max_length=256)]
    new_password: str

    @field_validator("new_password")
    @classmethod
    def _policy(cls, v: str) -> str:
        err = password_policy_error(v)
        if err:
            raise ValueError(err)
        return v


class MessageOut(BaseModel):
    message: str
