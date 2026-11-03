from datetime import datetime
from typing import Annotated, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ModerationListItem(BaseModel):
    id: UUID
    title: str
    topic: str
    source_url: str
    category_name: str
    status: str
    created_at: datetime


class ModerationDetail(BaseModel):
    id: UUID
    status: str
    title: str
    topic: str
    category_id: UUID
    category_name: str
    source_url: str
    canonical_url: str
    provider: str | None
    version: str
    edition_year: int
    instructors: str
    has_quizzes: bool
    requires_exam: bool
    offers_certificate: bool
    is_endorsed: bool
    endorsing_organization: str | None
    contributor_completed: bool
    contributor_id: UUID  # identificador interno, solo visible para moderación
    rejection_reason: str | None
    reviewed_by: UUID | None
    reviewed_at: datetime | None
    created_at: datetime


class DecisionIn(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    decision: Literal["approved", "rejected"]
    reason: Annotated[str, Field(max_length=1000)] | None = None
