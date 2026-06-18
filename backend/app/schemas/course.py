from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel

from app.constants.enums import CourseLevel, CourseStatus
from app.schemas.chapter import ChapterResponse
from app.schemas.user import UserResponse


class CourseBase(BaseModel):
    title: str
    description: str
    category: str
    level: CourseLevel
    price: Decimal
    cover_image: str


class CourseCreate(CourseBase):
    pass


class CourseUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    category: str | None = None
    level: CourseLevel | None = None
    price: Decimal | None = None
    cover_image: str | None = None


class CourseStatusUpdate(BaseModel):
    status: CourseStatus


class CourseResponse(CourseBase):
    id: int
    instructor_id: int
    total_lessons: int
    total_duration: int
    status: CourseStatus
    rating: float
    student_count: int
    created_at: datetime
    updated_at: datetime
    instructor: UserResponse | None = None

    model_config = {"from_attributes": True}


class CourseDetailResponse(CourseResponse):
    chapters: list[ChapterResponse] = []
