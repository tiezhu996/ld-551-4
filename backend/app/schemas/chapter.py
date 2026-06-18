from pydantic import BaseModel

from app.schemas.lesson import LessonResponse


class ChapterBase(BaseModel):
    title: str
    sort_order: int = 0


class ChapterCreate(ChapterBase):
    course_id: int


class ChapterResponse(ChapterBase):
    id: int
    course_id: int
    lessons: list[LessonResponse] = []

    model_config = {"from_attributes": True}
