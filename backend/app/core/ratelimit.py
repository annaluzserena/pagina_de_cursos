"""Rate limiting server-side persistido en PostgreSQL (TRD TD-002, §5.1).

Los contadores usan ventanas deslizantes sobre `login_attempts`. La comprobación y
el registro ocurren en la misma transacción, protegidos por un advisory lock por
clave (`pg_advisory_xact_lock`), de modo que el incremento es atómico. No hay
bloqueos permanentes: al salir de la ventana el contador se libera solo.
"""
import math
import random
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Literal

from sqlalchemy import delete, func, select, text
from sqlalchemy.orm import Session

from app.auth.models import LoginAttempt
from app.core.config import get_settings
from app.core.errors import rate_limited
from app.core.security import hmac_identifier


@dataclass(frozen=True)
class Rule:
    kind: Literal["subject", "ip"]
    max_attempts: int
    window_seconds: int


def identifier_hash(value: str) -> str:
    return hmac_identifier(value)


def _lock(db: Session, key: str) -> None:
    if db.get_bind().dialect.name == "postgresql":
        db.execute(text("SELECT pg_advisory_xact_lock(hashtextextended(:k, 0))"), {"k": key})


def check(
    db: Session,
    *,
    action: str,
    subject_hash: str,
    ip_hash: str,
    rules: list[Rule],
    failures_only: bool = False,
) -> None:
    """Toma los locks y lanza 429 si alguna regla se excede. El lock dura hasta el commit."""
    keys = sorted({f"{action}:{r.kind}:{subject_hash if r.kind == 'subject' else ip_hash}" for r in rules})
    for key in keys:
        _lock(db, key)

    now = datetime.now(UTC)
    for rule in rules:
        column = LoginAttempt.subject_hash if rule.kind == "subject" else LoginAttempt.ip_hash
        value = subject_hash if rule.kind == "subject" else ip_hash
        since = now - timedelta(seconds=rule.window_seconds)
        conds = [LoginAttempt.action == action, column == value, LoginAttempt.attempted_at > since]
        if failures_only:
            conds.append(LoginAttempt.succeeded.is_(False))
        count = db.scalar(select(func.count(LoginAttempt.id)).where(*conds)) or 0
        if count >= rule.max_attempts:
            oldest = db.scalar(select(func.min(LoginAttempt.attempted_at)).where(*conds))
            retry = 1
            if oldest is not None:
                retry = max(1, math.ceil((oldest + timedelta(seconds=rule.window_seconds) - now).total_seconds()))
            db.rollback()  # libera locks; no se registra nada
            raise rate_limited(retry)


def record(db: Session, *, action: str, subject_hash: str, ip_hash: str, succeeded: bool) -> None:
    db.add(
        LoginAttempt(
            action=action,
            subject_hash=subject_hash,
            ip_hash=ip_hash,
            succeeded=succeeded,
            attempted_at=datetime.now(UTC),
        )
    )
    if random.random() < 0.02:
        purge_old(db)


def check_and_record(
    db: Session, *, action: str, subject_hash: str, ip_hash: str, rules: list[Rule]
) -> None:
    """Para acciones donde cada solicitud cuenta (registro, recuperación, aportes)."""
    check(db, action=action, subject_hash=subject_hash, ip_hash=ip_hash, rules=rules)
    record(db, action=action, subject_hash=subject_hash, ip_hash=ip_hash, succeeded=True)
    db.commit()


def purge_old(db: Session) -> None:
    """Retención corta de intentos detallados (BackendSchema §1.2)."""
    cutoff = datetime.now(UTC) - timedelta(hours=get_settings().rl_retention_hours)
    db.execute(delete(LoginAttempt).where(LoginAttempt.attempted_at < cutoff))
