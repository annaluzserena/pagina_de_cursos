import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    SmallInteger,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.categories.models import Category
from app.core.db import Base


class Course(Base):
    __tablename__ = "courses"
    __table_args__ = (
        CheckConstraint("status IN ('pending_review', 'published', 'rejected')", name="status"),
        CheckConstraint("edition_year >= 1900", name="edition_year_min"),
        CheckConstraint(
            "status <> 'rejected' OR (rejection_reason IS NOT NULL AND length(btrim(rejection_reason)) > 0)",
            name="rejected_has_reason",
        ),
        CheckConstraint(
            "status <> 'published' OR (reviewed_by IS NOT NULL AND reviewed_at IS NOT NULL)",
            name="published_has_review",
        ),
        CheckConstraint(
            "NOT is_endorsed OR (endorsing_organization IS NOT NULL AND length(btrim(endorsing_organization)) > 0)",
            name="endorsed_has_organization",
        ),
        Index("ix_courses_status_created_at", "status", "created_at"),
        Index("ix_courses_category_status", "category_id", "status"),
        Index("ix_courses_title", "title"),
        Index("ix_courses_contributor_created_at", "contributor_id", "created_at"),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    contributor_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    category_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("categories.id"), nullable=False)
    canonical_url: Mapped[str] = mapped_column(String(2048), unique=True, nullable=False)
    source_url: Mapped[str] = mapped_column(String(2048), nullable=False)
    provider: Mapped[str | None] = mapped_column(String(160), nullable=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    topic: Mapped[str] = mapped_column(String(160), nullable=False)
    version: Mapped[str] = mapped_column(String(80), nullable=False)
    edition_year: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    instructors: Mapped[str] = mapped_column(Text, nullable=False)
    has_quizzes: Mapped[bool] = mapped_column(Boolean, nullable=False)
    requires_exam: Mapped[bool] = mapped_column(Boolean, nullable=False)
    offers_certificate: Mapped[bool] = mapped_column(Boolean, nullable=False)
    is_endorsed: Mapped[bool] = mapped_column(Boolean, nullable=False)
    endorsing_organization: Mapped[str | None] = mapped_column(String(200), nullable=True)
    contributor_completed: Mapped[bool] = mapped_column(Boolean, nullable=False)
    status: Mapped[str] = mapped_column(
        String(24), nullable=False, default="pending_review", server_default="pending_review"
    )
    rejection_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    reviewed_by: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )

    category: Mapped[Category] = relationship(lazy="joined")
