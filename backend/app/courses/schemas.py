"""Schemas de cursos. Las respuestas públicas nunca exponen al aportante (BackendSchema §4)."""
from datetime import UTC, datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictInt, field_validator

from app.courses.models import Course


class CourseOut(BaseModel):
    id: UUID
    title: str
    topic: str
    category_id: UUID
    category_name: str
    source_url: str
    provider: str | None
    version: str
    edition_year: int
    instructors: str
    has_quizzes: bool
    requires_exam: bool
    offers_certificate: bool
    is_endorsed: bool
    endorsing_organization: str | None
    contributor_completed: bool  # declaración agregada/no identificatoria (APPFlow §3)
    created_at: datetime


def course_out(c: Course) -> CourseOut:
    return CourseOut(
        id=c.id,
        title=c.title,
        topic=c.topic,
        category_id=c.category_id,
        category_name=c.category.name,
        source_url=c.source_url,
        provider=c.provider,
        version=c.version,
        edition_year=c.edition_year,
        instructors=c.instructors,
        has_quizzes=c.has_quizzes,
        requires_exam=c.requires_exam,
        offers_certificate=c.offers_certificate,
        is_endorsed=c.is_endorsed,
        endorsing_organization=c.endorsing_organization,
        contributor_completed=c.contributor_completed,
        created_at=c.created_at,
    )


Text = Annotated[str, Field(min_length=1)]


class ContributionIn(BaseModel):
    # extra=forbid: el cliente no puede enviar contributor_id, status, etc.
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    source_url: Annotated[str, Field(min_length=1, max_length=2048)]
    category_id: UUID
    topic: Annotated[str, Field(min_length=1, max_length=160)]
    title: Annotated[str, Field(min_length=1, max_length=200)]
    version: Annotated[str, Field(min_length=1, max_length=80)]
    edition_year: StrictInt
    instructors: Annotated[str, Field(min_length=1, max_length=500)]
    has_quizzes: StrictBool
    requires_exam: StrictBool
    offers_certificate: StrictBool
    is_endorsed: StrictBool
    endorsing_organization: Annotated[str, Field(max_length=200)] | None = None
    contributor_completed: StrictBool

    @field_validator("edition_year")
    @classmethod
    def _year_range(cls, v: int) -> int:  # BR-012
        max_year = datetime.now(UTC).year + 1
        if not 1900 <= v <= max_year:
            raise ValueError(f"El año debe estar entre 1900 y {max_year}.")
        return v


class ContributionCreated(BaseModel):
    id: UUID
    status: str
    title: str
    source_url: str
    created_at: datetime


class ContributionSummary(BaseModel):
    id: UUID
    title: str
    topic: str
    source_url: str
    category_name: str
    status: str
    rejection_reason: str | None
    created_at: datetime
    reviewed_at: datetime | None
