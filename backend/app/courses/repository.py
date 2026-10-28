"""Acceso a datos de cursos.

T2: datos hardcodeados en memoria. Se reemplaza por consultas SQLAlchemy cuando
existan los modelos y migraciones (M2). Solo se devuelven cursos `published`.
"""
from uuid import UUID

_CAT_PROG = UUID("00000000-0000-0000-0000-0000000000c1")
_CAT_DATOS = UUID("00000000-0000-0000-0000-0000000000c2")

_COURSES: list[dict] = [
    {
        "id": UUID("00000000-0000-0000-0000-000000000001"),
        "category_id": _CAT_PROG,
        "title": "CS50: Introduction to Computer Science",
        "topic": "Fundamentos de programación",
        "source_url": "https://cs50.harvard.edu/x/",
        "provider": "Harvard / edX",
        "version": "2025",
        "edition_year": 2025,
        "instructors": "David J. Malan",
        "has_quizzes": True,
        "requires_exam": False,
        "offers_certificate": True,
        "is_endorsed": True,
        "endorsing_organization": "Harvard University",
        "status": "published",
    },
    {
        "id": UUID("00000000-0000-0000-0000-000000000002"),
        "category_id": _CAT_DATOS,
        "title": "Introducción a SQL",
        "topic": "Bases de datos relacionales",
        "source_url": "https://example.org/cursos/sql-intro",
        "provider": "Ejemplo Academy",
        "version": "1.0",
        "edition_year": 2024,
        "instructors": "Equipo docente de ejemplo",
        "has_quizzes": True,
        "requires_exam": True,
        "offers_certificate": False,
        "is_endorsed": False,
        "endorsing_organization": None,
        "status": "published",
    },
    {
        # Pendiente: NO debe aparecer en el catálogo público (BR-001).
        "id": UUID("00000000-0000-0000-0000-000000000003"),
        "category_id": _CAT_PROG,
        "title": "Curso pendiente de revisión",
        "topic": "Ejemplo",
        "source_url": "https://example.org/cursos/pendiente",
        "provider": None,
        "version": "0.1",
        "edition_year": 2026,
        "instructors": "N/A",
        "has_quizzes": False,
        "requires_exam": False,
        "offers_certificate": False,
        "is_endorsed": False,
        "endorsing_organization": None,
        "status": "pending_review",
    },
]


def list_published(limit: int, offset: int) -> tuple[list[dict], int]:
    published = [c for c in _COURSES if c["status"] == "published"]
    # Orden estable: título y `id` como desempate (RNF-011).
    published.sort(key=lambda c: (c["title"].lower(), str(c["id"])))
    return published[offset : offset + limit], len(published)
