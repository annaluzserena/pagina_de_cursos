"""Seed idempotente: categorías, moderador de desarrollo y (opcional) datos demo.

Uso:  uv run python -m app.seed [--demo]
Las credenciales salen de SEED_MODERATOR_EMAIL / SEED_MODERATOR_PASSWORD (solo entorno local).
"""
import re
import sys
import unicodedata
from datetime import UTC, datetime, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth.models import User
from app.categories.models import Category
from app.core.config import get_settings
from app.core.db import get_session_factory
from app.core.security import hash_password, normalize_email, password_policy_error
from app.courses.models import Course
from app.courses.url import canonicalize

CATEGORIES = [
    "Programación", "Datos", "Sistemas", "Redes", "Seguridad",
    "Diseño", "Negocios", "Idiomas", "Ciencias", "Otros",
]


def slugify(name: str) -> str:
    base = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", base.lower()).strip("-")


def seed_categories(db: Session) -> None:
    existing = {c.slug for c in db.scalars(select(Category))}
    for name in CATEGORIES:
        if slugify(name) not in existing:
            db.add(Category(name=name, slug=slugify(name), is_active=True))
    db.flush()


def _ensure_user(db: Session, email: str, password: str, role: str) -> User:
    email = normalize_email(email)
    user = db.scalar(select(User).where(User.email == email))
    if user is None:
        user = User(email=email, password_hash=hash_password(password), role=role)
        db.add(user)
        db.flush()
    elif user.role != role:
        user.role = role
    return user


def seed_moderator(db: Session) -> User | None:
    s = get_settings()
    if not s.seed_moderator_email or not s.seed_moderator_password:
        print("• Moderador omitido: definí SEED_MODERATOR_EMAIL y SEED_MODERATOR_PASSWORD (solo local).")
        return None
    err = password_policy_error(s.seed_moderator_password)
    if err:
        raise SystemExit(f"SEED_MODERATOR_PASSWORD inválida: {err}")
    return _ensure_user(db, s.seed_moderator_email, s.seed_moderator_password, "moderator")


def seed_demo(db: Session, moderator: User) -> None:
    """>20 cursos publicados (para observar paginación) + casos pending/rejected."""
    contributor = _ensure_user(db, "demo.aportante@rutalibre.local", "demo-Password-123", "user")
    cats = {c.name: c for c in db.scalars(select(Category))}
    names = list(cats)
    now = datetime.now(UTC)

    def add(i: int, status: str) -> None:
        url = f"https://cursos-demo.example.org/curso-{i}"
        canonical, host = canonicalize(url)
        if db.scalar(select(Course.id).where(Course.canonical_url == canonical)):
            return
        course = Course(
            contributor_id=contributor.id,
            category_id=cats[names[i % len(names)]].id,
            canonical_url=canonical,
            source_url=url,
            provider=host,
            title=f"Curso demo {i:02d}: {names[i % len(names)]}",
            topic=f"Tema {i % 7 + 1}",
            version=f"{i % 3 + 1}.0",
            edition_year=2020 + i % 7,
            instructors=f"Docente {i}",
            has_quizzes=i % 2 == 0,
            requires_exam=i % 3 == 0,
            offers_certificate=i % 2 == 1,
            is_endorsed=i % 5 == 0,
            endorsing_organization="Universidad Demo" if i % 5 == 0 else None,
            contributor_completed=i % 4 != 0,
            status=status,
            created_at=now - timedelta(minutes=100 - i),
        )
        if status == "published":
            course.reviewed_by, course.reviewed_at = moderator.id, now
        elif status == "rejected":
            course.reviewed_by, course.reviewed_at = moderator.id, now
            course.rejection_reason = "La URL no corresponde a un curso gratuito."
        db.add(course)

    for i in range(1, 46):
        add(i, "published")
    for i in range(46, 49):
        add(i, "pending_review")
    for i in range(49, 51):
        add(i, "rejected")


def run(demo: bool = False) -> None:
    with get_session_factory()() as db:
        seed_categories(db)
        moderator = seed_moderator(db)
        if demo:
            if moderator is None:
                raise SystemExit("--demo requiere moderador: definí las variables SEED_MODERATOR_*.")
            seed_demo(db, moderator)
        db.commit()
    print("Seed completado." + (" (con datos demo)" if demo else ""))


if __name__ == "__main__":
    run(demo="--demo" in sys.argv[1:])
