"""Hashing de contraseñas, tokens y HMAC de identificadores."""
import hashlib
import hmac
import re
import secrets

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError

from app.core.config import get_settings

PASSWORD_MIN = 10
PASSWORD_MAX = 128
PASSWORD_POLICY_TEXT = (
    f"La contraseña debe tener entre {PASSWORD_MIN} y {PASSWORD_MAX} caracteres, "
    "al menos una letra y un número."
)

_hasher = PasswordHasher()  # Argon2id por defecto
# Hash de relleno para igualar tiempos cuando el email no existe.
DUMMY_HASH = _hasher.hash("rutalibre-dummy-password-1")


def password_policy_error(password: str) -> str | None:
    if not (PASSWORD_MIN <= len(password) <= PASSWORD_MAX):
        return PASSWORD_POLICY_TEXT
    if not re.search(r"[^\W\d_]", password) or not re.search(r"\d", password):
        return PASSWORD_POLICY_TEXT
    return None


def hash_password(password: str) -> str:
    return _hasher.hash(password)


def verify_password(password_hash: str, password: str) -> bool:
    try:
        return _hasher.verify(password_hash, password)
    except (VerificationError, InvalidHashError):
        return False


def new_token() -> str:
    return secrets.token_urlsafe(32)


def hash_token(token: str) -> str:
    """Hash de tokens de sesión/recuperación (alta entropía: SHA-256 es suficiente)."""
    return hashlib.sha256(token.encode()).hexdigest()


def hmac_identifier(value: str) -> str:
    """HMAC con secreto de configuración: contadores sin persistir email/IP en claro."""
    key = get_settings().secret_key.encode()
    return hmac.new(key, value.encode(), hashlib.sha256).hexdigest()


def normalize_email(email: str) -> str:
    return email.strip().lower()
