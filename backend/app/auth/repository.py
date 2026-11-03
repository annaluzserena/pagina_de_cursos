from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import delete, select, update
from sqlalchemy.orm import Session

from app.auth.models import PasswordResetToken, SessionRecord, User


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.scalar(select(User).where(User.email == email))


def get_user(db: Session, user_id: UUID) -> User | None:
    return db.get(User, user_id)


def add_user(db: Session, user: User) -> None:
    db.add(user)
    db.flush()  # dispara UNIQUE(email) dentro de la transacción


def add_session(db: Session, record: SessionRecord) -> None:
    db.add(record)


def delete_session(db: Session, session_id: UUID) -> None:
    db.execute(delete(SessionRecord).where(SessionRecord.id == session_id))


def delete_user_sessions(db: Session, user_id: UUID) -> None:
    db.execute(delete(SessionRecord).where(SessionRecord.user_id == user_id))


def delete_expired_sessions(db: Session, user_id: UUID) -> None:
    db.execute(
        delete(SessionRecord).where(
            SessionRecord.user_id == user_id, SessionRecord.expires_at < datetime.now(UTC)
        )
    )


def invalidate_unused_reset_tokens(db: Session, user_id: UUID) -> None:
    db.execute(
        update(PasswordResetToken)
        .where(PasswordResetToken.user_id == user_id, PasswordResetToken.used_at.is_(None))
        .values(used_at=datetime.now(UTC))
    )


def add_reset_token(db: Session, token: PasswordResetToken) -> None:
    db.add(token)


def get_reset_token_for_update(db: Session, token_hash: str) -> PasswordResetToken | None:
    return db.scalar(
        select(PasswordResetToken).where(PasswordResetToken.token_hash == token_hash).with_for_update()
    )
