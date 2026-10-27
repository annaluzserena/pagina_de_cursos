"""Configuración inicial de conexión a PostgreSQL (solo config, sin queries).

El engine es perezoso: no conecta hasta la primera consulta, por lo que la API
arranca aunque la base no esté disponible todavía.
"""
from functools import lru_cache

from sqlalchemy import Engine, create_engine, text
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import get_settings


@lru_cache
def get_engine() -> Engine:
    return create_engine(get_settings().database_url, pool_pre_ping=True)


@lru_cache
def get_session_factory() -> sessionmaker[Session]:
    return sessionmaker(bind=get_engine(), expire_on_commit=False)


def get_db():
    """Dependencia FastAPI para endpoints que usen la BD (futuros módulos)."""
    with get_session_factory()() as session:
        yield session


def check_connection() -> bool:
    """Verifica conectividad con `SELECT 1`. Útil para diagnóstico."""
    try:
        with get_engine().connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception:
        return False
