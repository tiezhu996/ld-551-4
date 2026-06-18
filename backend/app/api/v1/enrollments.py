from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.enrollment import EnrollmentResponse, LessonProgressCreate, ProgressResponse
from app.services.enrollment_service import EnrollmentService

router = APIRouter(prefix="/enrollments", tags=["enrollments"])


@router.get("", response_model=list[EnrollmentResponse])
def list_enrollments(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return EnrollmentService.list_user_enrollments(db, user)


@router.get("/recent", response_model=list[EnrollmentResponse])
def recent(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return EnrollmentService.list_user_enrollments(db, user)[:5]


@router.get("/{course_id}/progress", response_model=ProgressResponse)
def get_progress(course_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    enrollment, completed, total = EnrollmentService.get_progress(db, user, course_id)
    return ProgressResponse(enrollment_id=enrollment.id, course_id=course_id, progress=enrollment.progress, completed_lessons=completed, total_lessons=total)


@router.post("/progress/complete", response_model=EnrollmentResponse)
def complete_lesson(payload: LessonProgressCreate, request: Request, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return EnrollmentService.complete_lesson(db, user, payload.lesson_id, payload.score, request.client.host if request.client else None)
