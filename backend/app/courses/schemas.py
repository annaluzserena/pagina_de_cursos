"""Schemas públicos de cursos. Nunca exponen datos del aportante (BackendSchema §4)."""
from uuid import UUID

from pydantic import BaseModel


class CourseOut(BaseModel):
    id: UUID
    title: str
    topic: str
    category_id: UUID
    source_url: str
    provider: str | None = None
    version: str
    edition_year: int
    instructors: str
    has_quizzes: bool
    requires_exam: bool
    offers_certificate: bool
    is_endorsed: bool
    endorsing_organization: str | None = None


class CoursePage(BaseModel):
    items: list[CourseOut]
    total: int
    limit: int
    offset: int
