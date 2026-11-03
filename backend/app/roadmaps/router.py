from uuid import UUID

from fastapi import APIRouter, Response

from app.core.deps import CurrentUser, DbSession
from app.core.pagination import Page, Pagination
from app.roadmaps import service
from app.roadmaps.schemas import (
    RoadmapAddIn,
    RoadmapItemOut,
    RoadmapStatus,
    RoadmapUpdateIn,
)

router = APIRouter(prefix="/me/roadmap", tags=["roadmap"])


@router.get("", response_model=Page[RoadmapItemOut])
def list_roadmap(
    db: DbSession, user: CurrentUser, page: Pagination, status: RoadmapStatus | None = None
) -> Page[RoadmapItemOut]:
    return service.list_items(db, user, page, status)


@router.post("", response_model=RoadmapItemOut, status_code=201)
def add_to_roadmap(body: RoadmapAddIn, db: DbSession, user: CurrentUser) -> RoadmapItemOut:
    return service.add_item(db, user, body.course_id)


@router.patch("/{item_id}", response_model=RoadmapItemOut)
def update_roadmap_item(
    item_id: UUID, body: RoadmapUpdateIn, db: DbSession, user: CurrentUser
) -> RoadmapItemOut:
    return service.update_status(db, user, item_id, body.status)


@router.delete("/{item_id}", status_code=204)
def delete_roadmap_item(item_id: UUID, db: DbSession, user: CurrentUser) -> Response:
    service.remove_item(db, user, item_id)
    return Response(status_code=204)
