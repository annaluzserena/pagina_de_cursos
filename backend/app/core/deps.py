"""Dependencias compartidas: sesión de BD, usuario actual y rol (RF-011)."""
from datetime import UTC, datetime
from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth.models import SessionRecord, User
from app.core.config import get_settings
from app.core.db import get_db
from app.core.errors import forbidden, unauthorized
from app.core.security import hash_token

DbSession = Annotated[Session, Depends(get_db)]


def client_ip(request: Request) -> str:
    if get_settings().trust_proxy_headers:
        forwarded = request.headers.get("x-forwarded-for")
        if forwarded:
            return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def get_current_session(request: Request, db: DbSession) -> SessionRecord:
    token = request.cookies.get(get_settings().cookie_name)
    if not token:
        raise unauthorized()
    record = db.scalar(
        select(SessionRecord).where(
            SessionRecord.token_hash == hash_token(token),
            SessionRecord.expires_at > datetime.now(UTC),
        )
    )
    if record is None or not record.user.is_active:
        raise unauthorized("Tu sesión no es válida o venció.")
    return record


CurrentSession = Annotated[SessionRecord, Depends(get_current_session)]


def get_current_user(session: CurrentSession) -> User:
    return session.user


CurrentUser = Annotated[User, Depends(get_current_user)]


def require_moderator(user: CurrentUser) -> User:
    if user.role != "moderator":
        raise forbidden()
    return user


Moderator = Annotated[User, Depends(require_moderator)]
ClientIp = Annotated[str, Depends(client_ip)]
