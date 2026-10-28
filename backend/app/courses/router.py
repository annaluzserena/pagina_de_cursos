from typing import Annotated

from fastapi import APIRouter, Query

from app.courses import service
from app.courses.schemas import CoursePage

router = APIRouter(prefix="/courses", tags=["courses"])


@router.get("", response_model=CoursePage)
def list_courses(
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> CoursePage:
    """Catálogo público: solo cursos `published`, paginado (RNF-001)."""
    return service.list_public_courses(limit, offset)
