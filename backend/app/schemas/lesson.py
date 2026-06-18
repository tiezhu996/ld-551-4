from pydantic import BaseModel

from app.constants.enums import LessonType


class LessonBase(BaseModel):
    title: str
    type: LessonType
    content: str
    duration: int
    is_free: bool = False
    sort_order: int = 0


class LessonCreate(LessonBase):
    chapter_id: int


class LessonUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    duration: int | None = None
    is_free: bool | None = None
    sort_order: int | None = None


class LessonResponse(LessonBase):
    id: int
    chapter_id: int

    model_config = {"from_attributes": True}
