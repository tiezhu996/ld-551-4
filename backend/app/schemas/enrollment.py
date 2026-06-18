from datetime import datetime

from pydantic import BaseModel

from app.schemas.course import CourseResponse


class EnrollmentResponse(BaseModel):
    id: int
    user_id: int
    course_id: int
    enrolled_at: datetime
    progress: float
    last_access_at: datetime
    course: CourseResponse | None = None

    model_config = {"from_attributes": True}


class LessonProgressCreate(BaseModel):
    lesson_id: int
    score: int | None = None


class ProgressResponse(BaseModel):
    enrollment_id: int
    course_id: int
    progress: float
    completed_lessons: int
    total_lessons: int
