from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Query

from app.core.deps import ClientIp, CurrentUser, DbSession
from app.core.pagination import Page, Pagination
from app.courses import service
from app.courses.schemas import (
    ContributionCreated,
    ContributionIn,
    ContributionSummary,
    CourseOut,
)

router = APIRouter(tags=["courses"])


@router.get("/courses", response_model=Page[CourseOut])
def list_courses(
    db: DbSession,
    page: Pagination,
    q: Annotated[str | None, Query(max_length=100)] = None,
    category_id: UUID | None = None,
    topic: Annotated[str | None, Query(max_length=160)] = None,
    offers_certificate: bool | None = None,
) -> Page[CourseOut]:
    """Catálogo público: solo cursos `published`, paginado y filtrable."""
    return service.list_public(
        db, page, q=q.strip() or None if q else None, category_id=category_id,
        topic=topic.strip() or None if topic else None, offers_certificate=offers_certificate,
    )


@router.get("/courses/{course_id}", response_model=CourseOut)
def get_course(course_id: UUID, db: DbSession) -> CourseOut:
    return service.get_public(db, course_id)


@router.post("/contributions", response_model=ContributionCreated, status_code=201)
def create_contribution(
    body: ContributionIn, db: DbSession, user: CurrentUser, ip: ClientIp
) -> ContributionCreated:
    return service.create_contribution(db, user, body, ip)


@router.get("/me/contributions", response_model=Page[ContributionSummary])
def my_contributions(db: DbSession, user: CurrentUser, page: Pagination) -> Page[ContributionSummary]:
    return service.list_my_contributions(db, user, page)
