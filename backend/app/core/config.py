"""Configuración por entorno (TRD §4: sin secretos en el repo)."""
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

_DEV_SECRET = "dev-only-change-me-secret-key-0000000000"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    environment: str = "development"  # development | production
    database_url: str = "postgresql+psycopg://rutalibre:change_me@localhost:5432/rutalibre"
    # Lista separada por comas. Nunca "*" junto con credenciales (TRD §4).
    cors_origins: str = "http://localhost:5173"
    # Secreto para HMAC de identificadores (IP/email) en el rate limit.
    secret_key: str = _DEV_SECRET

    # Sesión (cookie opaca HttpOnly, SameSite=Lax; Secure solo en HTTPS).
    cookie_name: str = "rutalibre_session"
    cookie_secure: bool = False
    session_ttl_minutes: int = 60 * 24 * 7
    trust_proxy_headers: bool = False  # usar X-Forwarded-For solo detrás de proxy confiable

    # Recuperación de contraseña (BackendSchema: 30 min, un solo uso).
    password_reset_ttl_minutes: int = 30
    frontend_base_url: str = "http://localhost:5173"

    # Email (SMTP configurable; Mailpit en desarrollo).
    smtp_host: str = "localhost"
    smtp_port: int = 1025
    smtp_user: str = ""
    smtp_password: str = ""
    smtp_starttls: bool = False
    mail_from: str = "RutaLibre <no-reply@rutalibre.local>"

    # Rate limiting (TRD §5.1). Ventana en segundos.
    rl_window_seconds: int = 15 * 60
    rl_login_per_identifier: int = 5
    rl_login_per_ip: int = 20
    rl_register_per_ip: int = 5
    rl_forgot_per_ip: int = 5
    rl_forgot_per_email: int = 5
    rl_reset_per_ip: int = 10
    rl_contribute_per_user: int = 10
    rl_contribute_window_seconds: int = 60 * 60
    rl_retention_hours: int = 48

    # Seed (solo entorno local; nunca credenciales reales).
    seed_moderator_email: str = "moderadora@rutalibre.local"
    seed_moderator_password: str = "Moderadora-Local-123"

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    def validate_for_runtime(self) -> None:
        if self.environment == "production":
            if self.secret_key == _DEV_SECRET or len(self.secret_key) < 32:
                raise RuntimeError("SECRET_KEY seguro es obligatorio en producción.")
            if not self.cookie_secure:
                raise RuntimeError("COOKIE_SECURE=true es obligatorio en producción.")


@lru_cache
def get_settings() -> Settings:
    return Settings()
