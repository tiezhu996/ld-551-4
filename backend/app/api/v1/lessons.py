from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import require_role
from app.constants.enums import UserRole
from app.core.database import get_db
from app.schemas.chapter import ChapterCreate, ChapterResponse
from app.schemas.lesson import LessonCreate, LessonResponse, LessonUpdate
from app.services.lesson_service import LessonService

router = APIRouter(prefix="/lessons", tags=["lessons"])


@router.get("/{lesson_id}", response_model=LessonResponse)
def get_lesson(lesson_id: int, db: Session = Depends(get_db)):
    return LessonService.get_lesson(db, lesson_id)


@router.post("/chapters", response_model=ChapterResponse)
def create_chapter(payload: ChapterCreate, _: object = Depends(require_role(UserRole.INSTRUCTOR, UserRole.ADMIN)), db: Session = Depends(get_db)):
    return LessonService.create_chapter(db, payload)


@router.post("", response_model=LessonResponse)
def create_lesson(payload: LessonCreate, _: object = Depends(require_role(UserRole.INSTRUCTOR, UserRole.ADMIN)), db: Session = Depends(get_db)):
    return LessonService.create_lesson(db, payload)


@router.put("/{lesson_id}", response_model=LessonResponse)
def update_lesson(lesson_id: int, payload: LessonUpdate, _: object = Depends(require_role(UserRole.INSTRUCTOR, UserRole.ADMIN)), db: Session = Depends(get_db)):
    return LessonService.update_lesson(db, lesson_id, payload)
