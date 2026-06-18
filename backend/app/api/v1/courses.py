from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_role
from app.constants.enums import CourseStatus, UserRole
from app.core.database import get_db
from app.models.user import User
from app.schemas.chapter import ChapterResponse
from app.schemas.common import PageResponse
from app.schemas.course import CourseCreate, CourseDetailResponse, CourseResponse, CourseStatusUpdate, CourseUpdate
from app.services.course_service import CourseService

router = APIRouter(prefix="/courses", tags=["courses"])


@router.get("", response_model=PageResponse[CourseResponse])
def list_courses(
    category: str | None = None,
    level: str | None = None,
    keyword: str | None = None,
    sort: str = "latest",
    page: int = 1,
    size: int = 12,
    db: Session = Depends(get_db),
):
    total, items = CourseService.list_published(db, category=category, level=level, keyword=keyword, sort=sort, page=page, size=size)
    return PageResponse(total=total, page=page, size=size, items=items)


@router.get("/{course_id}", response_model=CourseDetailResponse)
def get_course(course_id: int, db: Session = Depends(get_db)):
    return CourseService.get_course(db, course_id)


@router.get("/{course_id}/chapters", response_model=list[ChapterResponse])
def get_chapters(course_id: int, db: Session = Depends(get_db)):
    return CourseService.get_course(db, course_id).chapters


@router.post("", response_model=CourseResponse)
def create_course(
    payload: CourseCreate,
    request: Request,
    user: User = Depends(require_role(UserRole.INSTRUCTOR, UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    return CourseService.create_course(db, user, payload, request.client.host if request.client else None)


@router.put("/{course_id}", response_model=CourseResponse)
def update_course(
    course_id: int,
    payload: CourseUpdate,
    request: Request,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return CourseService.update_course(db, user, course_id, payload, request.client.host if request.client else None)


@router.patch("/{course_id}/status", response_model=CourseResponse)
def update_course_status(
    course_id: int,
    payload: CourseStatusUpdate,
    request: Request,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if payload.status == CourseStatus.PUBLISHED:
        require_role(UserRole.ADMIN)(user)
    return CourseService.change_status(db, user, course_id, payload.status, request.client.host if request.client else None)
