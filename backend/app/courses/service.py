from app.courses import repository
from app.courses.schemas import CourseOut, CoursePage


def list_public_courses(limit: int, offset: int) -> CoursePage:
    rows, total = repository.list_published(limit, offset)
    return CoursePage(
        items=[CourseOut(**row) for row in rows],
        total=total,
        limit=limit,
        offset=offset,
    )
