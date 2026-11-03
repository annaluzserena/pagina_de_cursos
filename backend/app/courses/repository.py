from uuid import UUID

from sqlalchemy import ColumnElement, func, or_, select
from sqlalchemy.orm import Session

from app.core.pagination import PageParams
from app.courses.models import Course


def _escape_like(value: str) -> str:
    return value.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")


def _published_conditions(
    q: str | None, category_id: UUID | None, topic: str | None, offers_certificate: bool | None
) -> list[ColumnElement[bool]]:
    conds: list[ColumnElement[bool]] = [Course.status == "published"]
    if q:
        pattern = f"%{_escape_like(q)}%"  # parametrizado: nunca se concatena SQL
        conds.append(
            or_(
                Course.title.ilike(pattern, escape="\\"),
                Course.topic.ilike(pattern, escape="\\"),
                Course.instructors.ilike(pattern, escape="\\"),
                Course.provider.ilike(pattern, escape="\\"),
            )
        )
    if category_id:
        conds.append(Course.category_id == category_id)
    if topic:
        conds.append(func.lower(Course.topic) == topic.lower())
    if offers_certificate is not None:
        conds.append(Course.offers_certificate.is_(offers_certificate))
    return conds


def list_published(
    db: Session,
    p: PageParams,
    *,
    q: str | None,
    category_id: UUID | None,
    topic: str | None,
    offers_certificate: bool | None,
) -> tuple[list[Course], int]:
    conds = _published_conditions(q, category_id, topic, offers_certificate)
    total = db.scalar(select(func.count(Course.id)).where(*conds)) or 0
    rows = db.scalars(
        select(Course)
        .where(*conds)
        .order_by(Course.created_at.desc(), Course.id.desc())
        .limit(p.limit)
        .offset(p.offset)
    ).all()
    return list(rows), total


def get_published(db: Session, course_id: UUID) -> Course | None:
    return db.scalar(select(Course).where(Course.id == course_id, Course.status == "published"))


def get_by_canonical_url(db: Session, canonical_url: str) -> Course | None:
    return db.scalar(select(Course.id).where(Course.canonical_url == canonical_url))


def add(db: Session, course: Course) -> None:
    db.add(course)
    db.flush()  # dispara UNIQUE(canonical_url) dentro de la transacción


def list_by_contributor(db: Session, user_id: UUID, p: PageParams) -> tuple[list[Course], int]:
    total = db.scalar(select(func.count(Course.id)).where(Course.contributor_id == user_id)) or 0
    rows = db.scalars(
        select(Course)
        .where(Course.contributor_id == user_id)
        .order_by(Course.created_at.desc(), Course.id.desc())
        .limit(p.limit)
        .offset(p.offset)
    ).all()
    return list(rows), total


