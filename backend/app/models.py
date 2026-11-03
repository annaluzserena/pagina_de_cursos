"""Importa todos los modelos para que Alembic vea el metadata completo."""
from app.auth.models import LoginAttempt, PasswordResetToken, SessionRecord, User  # noqa: F401
from app.categories.models import Category  # noqa: F401
from app.courses.models import Course  # noqa: F401
from app.moderation.models import ModerationDecision  # noqa: F401
from app.roadmaps.models import RoadmapItem  # noqa: F401
