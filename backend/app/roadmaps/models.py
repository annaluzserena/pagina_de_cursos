import uuid
from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base
from app.courses.models import Course


class RoadmapItem(Base):
    __tablename__ = "roadmap_items"
    __table_args__ = (
        UniqueConstraint("user_id", "course_id", name="uq_roadmap_items_user_course"),
        CheckConstraint("status IN ('planned', 'in_progress', 'completed')", name="status"),
        Index("ix_roadmap_items_user_added_at", "user_id", "added_at"),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    course_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("courses.id"), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="planned", server_default="planned")
    added_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )

    course: Mapped[Course] = relationship(lazy="joined")
