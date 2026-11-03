from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.categories.models import Category
from app.core.pagination import PageParams


def list_active(db: Session, p: PageParams) -> tuple[list[Category], int]:
    total = db.scalar(select(func.count(Category.id)).where(Category.is_active.is_(True))) or 0
    rows = db.scalars(
        select(Category)
        .where(Category.is_active.is_(True))
        .order_by(Category.name, Category.id)
        .limit(p.limit)
        .offset(p.offset)
    ).all()
    return list(rows), total


def get_active(db: Session, category_id: UUID) -> Category | None:
    return db.scalar(select(Category).where(Category.id == category_id, Category.is_active.is_(True)))
