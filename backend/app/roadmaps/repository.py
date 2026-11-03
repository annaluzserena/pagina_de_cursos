from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.pagination import PageParams
from app.courses.models import Course
from app.roadmaps.models import RoadmapItem


def list_for_user(
    db: Session, user_id: UUID, p: PageParams, status: str | None
) -> tuple[list[RoadmapItem], int]:
    conds = [RoadmapItem.user_id == user_id, Course.status == "published"]
    if status:
        conds.append(RoadmapItem.status == status)
    total = db.scalar(
        select(func.count(RoadmapItem.id)).join(Course, Course.id == RoadmapItem.course_id).where(*conds)
    ) or 0
    rows = db.scalars(
        select(RoadmapItem)
        .join(Course, Course.id == RoadmapItem.course_id)
        .where(*conds)
        .order_by(RoadmapItem.added_at.desc(), RoadmapItem.id.desc())
        .limit(p.limit)
        .offset(p.offset)
    ).all()
    return list(rows), total


def get_owned(db: Session, user_id: UUID, item_id: UUID) -> RoadmapItem | None:
    # La propiedad se decide siempre con el usuario de la sesión.
    return db.scalar(select(RoadmapItem).where(RoadmapItem.id == item_id, RoadmapItem.user_id == user_id))


def exists(db: Session, user_id: UUID, course_id: UUID) -> bool:
    return db.scalar(
        select(RoadmapItem.id).where(RoadmapItem.user_id == user_id, RoadmapItem.course_id == course_id)
    ) is not None


def add(db: Session, item: RoadmapItem) -> None:
    db.add(item)
    db.flush()
