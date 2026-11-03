"""Catálogo público y aportes (RF-005..007, RF-009)."""
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.auth.models import User
from app.categories import repository as categories
from app.core import ratelimit
from app.core.config import get_settings
from app.core.errors import conflict, not_found, validation_error
from app.core.pagination import Page, PageParams
from app.core.ratelimit import Rule
from app.courses import repository
from app.courses.models import Course
from app.courses.schemas import (
    ContributionCreated,
    ContributionIn,
    ContributionSummary,
    CourseOut,
    course_out,
)
from app.courses.url import canonicalize

DUPLICATE_MSG = "Ya existe un curso con esa URL en RutaLibre."


def list_public(
    db: Session,
    p: PageParams,
    *,
    q: str | None,
    category_id: UUID | None,
    topic: str | None,
    offers_certificate: bool | None,
) -> Page[CourseOut]:
    rows, total = repository.list_published(
        db, p, q=q, category_id=category_id, topic=topic, offers_certificate=offers_certificate
    )
    return Page[CourseOut](items=[course_out(c) for c in rows], total=total, limit=p.limit, offset=p.offset)


def get_public(db: Session, course_id: UUID) -> CourseOut:
    course = repository.get_published(db, course_id)
    if course is None:  # inexistente y no publicado son indistinguibles
        raise not_found("Curso no encontrado.")
    return course_out(course)


def create_contribution(db: Session, user: User, data: ContributionIn, ip: str) -> ContributionCreated:
    s = get_settings()
    subject_hash = ratelimit.identifier_hash(str(user.id))
    ip_hash = ratelimit.identifier_hash(ip)
    # Solo cuentan los aportes aceptados: corregir errores de validación no consume el cupo.
    ratelimit.check(
        db,
        action="contribute",
        subject_hash=subject_hash,
        ip_hash=ip_hash,
        rules=[Rule("subject", s.rl_contribute_per_user, s.rl_contribute_window_seconds)],
    )

    errors: dict[str, str] = {}
    canonical = host = None
    try:
        canonical, host = canonicalize(data.source_url)
    except ValueError as exc:
        errors["source_url"] = str(exc)
    if categories.get_active(db, data.category_id) is None:
        errors["category_id"] = "La categoría no existe o no está activa."
    org = (data.endorsing_organization or "").strip() or None
    if data.is_endorsed and not org:  # BR-006
        errors["endorsing_organization"] = "Indicá qué organización avala el curso."
    if errors:
        raise validation_error(errors)
    assert canonical and host

    if repository.get_by_canonical_url(db, canonical):
        raise conflict("duplicate_url", DUPLICATE_MSG)

    course = Course(
        contributor_id=user.id,  # siempre desde la sesión, nunca del cliente
        category_id=data.category_id,
        canonical_url=canonical,
        source_url=data.source_url.strip(),
        provider=host[:160],
        title=data.title,
        topic=data.topic,
        version=data.version,
        edition_year=data.edition_year,
        instructors=data.instructors,
        has_quizzes=data.has_quizzes,
        requires_exam=data.requires_exam,
        offers_certificate=data.offers_certificate,
        is_endorsed=data.is_endorsed,
        endorsing_organization=org if data.is_endorsed else None,
        contributor_completed=data.contributor_completed,
        status="pending_review",  # BR-007: nunca se publica automáticamente
    )
    try:
        repository.add(db, course)
        ratelimit.record(db, action="contribute", subject_hash=subject_hash, ip_hash=ip_hash, succeeded=True)
        db.commit()  # aporte + contador en la misma transacción
    except IntegrityError:  # carrera entre dos envíos de la misma URL
        db.rollback()
        raise conflict("duplicate_url", DUPLICATE_MSG) from None
    return ContributionCreated(
        id=course.id,
        status=course.status,
        title=course.title,
        source_url=course.source_url,
        created_at=course.created_at,
    )


def list_my_contributions(db: Session, user: User, p: PageParams) -> Page[ContributionSummary]:
    rows, total = repository.list_by_contributor(db, user.id, p)
    items = [
        ContributionSummary(
            id=c.id,
            title=c.title,
            topic=c.topic,
            source_url=c.source_url,
            category_name=c.category.name,
            status=c.status,
            rejection_reason=c.rejection_reason,
            created_at=c.created_at,
            reviewed_at=c.reviewed_at,
        )
        for c in rows
    ]
    return Page[ContributionSummary](items=items, total=total, limit=p.limit, offset=p.offset)
