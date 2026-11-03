"""Roadmap personal (RF-010, US-006/007). Todo se filtra por el usuario de la sesión."""
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.auth.models import User
from app.core.errors import conflict, not_found
from app.core.pagination import Page, PageParams
from app.courses import repository as courses
from app.roadmaps import repository
from app.roadmaps.models import RoadmapItem
from app.roadmaps.schemas import RoadmapItemOut, item_out

ALREADY = "Ya está en tu roadmap."


def list_items(db: Session, user: User, p: PageParams, status: str | None) -> Page[RoadmapItemOut]:
    rows, total = repository.list_for_user(db, user.id, p, status)
    return Page[RoadmapItemOut](items=[item_out(i) for i in rows], total=total, limit=p.limit, offset=p.offset)


def add_item(db: Session, user: User, course_id: UUID) -> RoadmapItemOut:
    if courses.get_published(db, course_id) is None:  # el estado se valida en el momento de agregar
        raise not_found("Curso no encontrado.")
    if repository.exists(db, user.id, course_id):
        raise conflict("already_in_roadmap", ALREADY)
    item = RoadmapItem(user_id=user.id, course_id=course_id, status="planned")
    try:
        repository.add(db, item)
        db.commit()
    except IntegrityError:  # doble clic / carrera: UNIQUE(user_id, course_id)
        db.rollback()
        raise conflict("already_in_roadmap", ALREADY) from None
    db.refresh(item)
    return item_out(item)


def update_status(db: Session, user: User, item_id: UUID, status: str) -> RoadmapItemOut:
    item = repository.get_owned(db, user.id, item_id)
    if item is None:  # inexistente o ajeno: misma respuesta, sin filtrar información
        raise not_found("Elemento no encontrado.")
    item.status = status
    db.commit()
    db.refresh(item)
    return item_out(item)


def remove_item(db: Session, user: User, item_id: UUID) -> None:
    item = repository.get_owned(db, user.id, item_id)
    if item is None:
        raise not_found("Elemento no encontrado.")
    db.delete(item)
    db.commit()
