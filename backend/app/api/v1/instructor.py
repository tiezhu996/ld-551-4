from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import require_role
from app.constants.enums import UserRole
from app.core.database import get_db
from app.models.user import User
from app.schemas.course import CourseResponse
from app.services.course_service import CourseService

router = APIRouter(prefix="/instructor", tags=["instructor"])


@router.get("/courses", response_model=list[CourseResponse])
def instructor_courses(user: User = Depends(require_role(UserRole.INSTRUCTOR, UserRole.ADMIN)), db: Session = Depends(get_db)):
    return CourseService.instructor_courses(db, user)
