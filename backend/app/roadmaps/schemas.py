from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.courses.schemas import CourseOut, course_out
from app.roadmaps.models import RoadmapItem

RoadmapStatus = Literal["planned", "in_progress", "completed"]


class RoadmapAddIn(BaseModel):
    model_config = ConfigDict(extra="forbid")  # nunca se acepta user_id del cliente
    course_id: UUID


class RoadmapUpdateIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    status: RoadmapStatus


class RoadmapItemOut(BaseModel):
    id: UUID
    status: str
    added_at: datetime
    updated_at: datetime
    course: CourseOut


def item_out(i: RoadmapItem) -> RoadmapItemOut:
    return RoadmapItemOut(
        id=i.id, status=i.status, added_at=i.added_at, updated_at=i.updated_at, course=course_out(i.course)
    )
