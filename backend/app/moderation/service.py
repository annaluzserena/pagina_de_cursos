"""Revisión de aportes (RF-008, US-009). Decisión transaccional y auditada."""
from datetime import UTC, datetime
from typing import Literal
from uuid import UUID

from sqlalchemy.orm import Session

from app.auth.models import User
from app.core.errors import conflict, not_found, validation_error
from app.core.pagination import Page, PageParams
from app.courses.models import Course
from app.moderation import repository
from app.moderation.models import ModerationDecision
from app.moderation.schemas import DecisionIn, ModerationDetail, ModerationListItem


def _detail(c: Course) -> ModerationDetail:
    return ModerationDetail(
        id=c.id,
        status=c.status,
        title=c.title,
        topic=c.topic,
        category_id=c.category_id,
        category_name=c.category.name,
        source_url=c.source_url,
        canonical_url=c.canonical_url,
        provider=c.provider,
        version=c.version,
        edition_year=c.edition_year,
        instructors=c.instructors,
        has_quizzes=c.has_quizzes,
        requires_exam=c.requires_exam,
        offers_certificate=c.offers_certificate,
        is_endorsed=c.is_endorsed,
        endorsing_organization=c.endorsing_organization,
        contributor_completed=c.contributor_completed,
        contributor_id=c.contributor_id,
        rejection_reason=c.rejection_reason,
        reviewed_by=c.reviewed_by,
        reviewed_at=c.reviewed_at,
        created_at=c.created_at,
    )


def list_queue(
    db: Session, p: PageParams, status: Literal["pending_review", "published", "rejected"]
) -> Page[ModerationListItem]:
    rows, total = repository.list_by_status(db, status, p)
    items = [
        ModerationListItem(
            id=c.id, title=c.title, topic=c.topic, source_url=c.source_url,
            category_name=c.category.name, status=c.status, created_at=c.created_at,
        )
        for c in rows
    ]
    return Page[ModerationListItem](items=items, total=total, limit=p.limit, offset=p.offset)


def get_detail(db: Session, course_id: UUID) -> ModerationDetail:
    course = repository.get(db, course_id)
    if course is None:
        raise not_found("Aporte no encontrado.")
    return _detail(course)


def decide(db: Session, moderator: User, course_id: UUID, data: DecisionIn) -> ModerationDetail:
    reason = (data.reason or "").strip() or None
    if data.decision == "rejected" and not reason:
        raise validation_error({"reason": "El rechazo requiere un motivo."})

    # Bloqueo de fila: dos moderadores no pueden resolver el mismo aporte a la vez.
    course = repository.get_for_update(db, course_id)
    if course is None:
        db.rollback()
        raise not_found("Aporte no encontrado.")
    if course.status != "pending_review":
        db.rollback()
        raise conflict("already_resolved", "Este aporte ya fue resuelto por otra persona.")

    now = datetime.now(UTC)
    course.status = "published" if data.decision == "approved" else "rejected"
    course.rejection_reason = reason if data.decision == "rejected" else None
    course.reviewed_by = moderator.id
    course.reviewed_at = now
    repository.add_decision(
        db,
        ModerationDecision(
            course_id=course.id, moderator_id=moderator.id, decision=data.decision, reason=reason
        ),
    )
    db.commit()
    return _detail(course)
