"""Reglas de autenticación: registro, login, recuperación (RF-001..004, US-003/004)."""
from datetime import UTC, datetime, timedelta

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.auth import repository
from app.auth.models import PasswordResetToken, SessionRecord, User
from app.core import ratelimit
from app.core.config import get_settings
from app.core.errors import AppError, conflict
from app.core.mailer import send_email
from app.core.ratelimit import Rule
from app.core.security import (
    DUMMY_HASH,
    hash_password,
    hash_token,
    new_token,
    verify_password,
)

INVALID_CREDENTIALS = AppError(401, "invalid_credentials", "Email o contraseña incorrectos.")


def _create_session(db: Session, user: User) -> str:
    token = new_token()
    repository.add_session(
        db,
        SessionRecord(
            user_id=user.id,
            token_hash=hash_token(token),
            expires_at=datetime.now(UTC) + timedelta(minutes=get_settings().session_ttl_minutes),
        ),
    )
    return token


def register(db: Session, email: str, password: str, ip: str) -> tuple[User, str]:
    s = get_settings()
    ratelimit.check_and_record(
        db,
        action="register",
        subject_hash=ratelimit.identifier_hash(email),
        ip_hash=ratelimit.identifier_hash(ip),
        rules=[Rule("ip", s.rl_register_per_ip, s.rl_window_seconds)],
    )
    if repository.get_user_by_email(db, email):
        raise conflict("email_taken", "Ya existe una cuenta con ese email.")
    user = User(email=email, password_hash=hash_password(password), role="user")
    try:
        repository.add_user(db, user)
    except IntegrityError:
        db.rollback()
        raise conflict("email_taken", "Ya existe una cuenta con ese email.") from None
    token = _create_session(db, user)
    db.commit()  # usuario + sesión: operación atómica
    return user, token


def login(db: Session, email: str, password: str, ip: str) -> tuple[User, str]:
    s = get_settings()
    subject_hash = ratelimit.identifier_hash(email)
    ip_hash = ratelimit.identifier_hash(ip)

    # Cuenta solo fallos; aplica también a emails inexistentes (no revela existencia).
    ratelimit.check(
        db,
        action="login",
        subject_hash=subject_hash,
        ip_hash=ip_hash,
        failures_only=True,
        rules=[
            Rule("subject", s.rl_login_per_identifier, s.rl_window_seconds),
            Rule("ip", s.rl_login_per_ip, s.rl_window_seconds),
        ],
    )

    user = repository.get_user_by_email(db, email)
    ok = verify_password(user.password_hash if user else DUMMY_HASH, password)
    if not (user and ok and user.is_active):
        ratelimit.record(db, action="login", subject_hash=subject_hash, ip_hash=ip_hash, succeeded=False)
        db.commit()
        raise INVALID_CREDENTIALS

    ratelimit.record(db, action="login", subject_hash=subject_hash, ip_hash=ip_hash, succeeded=True)
    repository.delete_expired_sessions(db, user.id)
    token = _create_session(db, user)  # sesión nueva en cada login
    db.commit()
    return user, token


def logout(db: Session, session: SessionRecord) -> None:
    repository.delete_session(db, session.id)
    db.commit()


def request_password_reset(db: Session, email: str, ip: str) -> tuple[str, str] | None:
    """Devuelve (email, token) si corresponde enviar correo; la respuesta HTTP es siempre genérica."""
    s = get_settings()
    ratelimit.check_and_record(
        db,
        action="forgot",
        subject_hash=ratelimit.identifier_hash(email),
        ip_hash=ratelimit.identifier_hash(ip),
        rules=[
            Rule("ip", s.rl_forgot_per_ip, s.rl_window_seconds),
            Rule("subject", s.rl_forgot_per_email, s.rl_window_seconds),
        ],
    )
    user = repository.get_user_by_email(db, email)
    if not user or not user.is_active:
        return None
    repository.invalidate_unused_reset_tokens(db, user.id)  # solo el token más reciente vale
    token = new_token()
    repository.add_reset_token(
        db,
        PasswordResetToken(
            user_id=user.id,
            token_hash=hash_token(token),
            expires_at=datetime.now(UTC) + timedelta(minutes=s.password_reset_ttl_minutes),
        ),
    )
    db.commit()
    return user.email, token


def send_reset_email(email: str, token: str) -> None:
    s = get_settings()
    link = f"{s.frontend_base_url.rstrip('/')}/restablecer?token={token}"
    send_email(
        email,
        "Restablecer tu contraseña de RutaLibre",
        "Recibimos una solicitud para restablecer tu contraseña.\n\n"
        f"Abrí este enlace (vence en {s.password_reset_ttl_minutes} minutos y se puede usar una sola vez):\n"
        f"{link}\n\n"
        "Si no fuiste vos, ignorá este mensaje.",
    )


def reset_password(db: Session, token: str, new_password: str, ip: str) -> None:
    s = get_settings()
    ratelimit.check_and_record(
        db,
        action="reset",
        subject_hash=ratelimit.identifier_hash("-"),
        ip_hash=ratelimit.identifier_hash(ip),
        rules=[Rule("ip", s.rl_reset_per_ip, s.rl_window_seconds)],
    )
    invalid = AppError(400, "invalid_token", "El enlace es inválido, venció o ya fue usado.")
    record = repository.get_reset_token_for_update(db, hash_token(token))
    now = datetime.now(UTC)
    if record is None or record.used_at is not None or record.expires_at <= now:
        db.rollback()
        raise invalid
    user = repository.get_user(db, record.user_id)
    if user is None or not user.is_active:
        db.rollback()
        raise invalid

    # Una sola transacción: nueva contraseña + token consumido + sesiones invalidadas.
    user.password_hash = hash_password(new_password)
    record.used_at = now
    repository.invalidate_unused_reset_tokens(db, user.id)
    repository.delete_user_sessions(db, user.id)
    db.commit()
