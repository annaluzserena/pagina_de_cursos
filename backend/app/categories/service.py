from sqlalchemy.orm import Session

from app.categories import repository
from app.categories.schemas import CategoryOut
from app.core.pagination import Page, PageParams


def list_categories(db: Session, p: PageParams) -> Page[CategoryOut]:
    rows, total = repository.list_active(db, p)
    return Page[CategoryOut](
        items=[CategoryOut.model_validate(r) for r in rows], total=total, limit=p.limit, offset=p.offset
    )
