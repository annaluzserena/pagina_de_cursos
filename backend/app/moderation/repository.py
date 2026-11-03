from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.pagination import PageParams
from app.courses.models import Course
from app.moderation.models import ModerationDecision


def list_by_status(db: Session, status: str, p: PageParams) -> tuple[list[Course], int]:
    total = db.scalar(select(func.count(Course.id)).where(Course.status == status)) or 0
    rows = db.scalars(
        select(Course)
        .where(Course.status == status)
        .order_by(Course.created_at.asc(), Course.id.asc())  # la cola atiende primero lo más antiguo
        .limit(p.limit)
        .offset(p.offset)
    ).all()
    return list(rows), total


def get(db: Session, course_id: UUID) -> Course | None:
    return db.get(Course, course_id)


def get_for_update(db: Session, course_id: UUID) -> Course | None:
    # of=Course: bloquea solo la fila del curso (la categoría se une por JOIN).
    return db.scalar(select(Course).where(Course.id == course_id).with_for_update(of=Course))


def add_decision(db: Session, decision: ModerationDecision) -> None:
    db.add(decision)
