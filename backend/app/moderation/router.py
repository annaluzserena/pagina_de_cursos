from typing import Literal
from uuid import UUID

from fastapi import APIRouter

from app.core.deps import DbSession, Moderator
from app.core.pagination import Page, Pagination
from app.moderation import service
from app.moderation.schemas import DecisionIn, ModerationDetail, ModerationListItem

router = APIRouter(prefix="/moderation", tags=["moderation"])


@router.get("/contributions", response_model=Page[ModerationListItem])
def list_contributions(
    db: DbSession,
    _: Moderator,
    page: Pagination,
    status: Literal["pending_review", "published", "rejected"] = "pending_review",
) -> Page[ModerationListItem]:
    return service.list_queue(db, page, status)


@router.get("/contributions/{contribution_id}", response_model=ModerationDetail)
def get_contribution(contribution_id: UUID, db: DbSession, _: Moderator) -> ModerationDetail:
    return service.get_detail(db, contribution_id)


@router.post("/contributions/{contribution_id}/decision", response_model=ModerationDetail)
def decide(
    contribution_id: UUID, body: DecisionIn, db: DbSession, moderator: Moderator
) -> ModerationDetail:
    return service.decide(db, moderator, contribution_id, body)
