from fastapi import APIRouter

from app.categories import service
from app.categories.schemas import CategoryOut
from app.core.deps import DbSession
from app.core.pagination import Page, Pagination

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("", response_model=Page[CategoryOut])
def list_categories(db: DbSession, page: Pagination) -> Page[CategoryOut]:
    return service.list_categories(db, page)
