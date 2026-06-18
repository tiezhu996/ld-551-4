from sqlalchemy import Boolean, Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.constants.enums import LessonType
from app.core.database import Base


class Lesson(Base):
    __tablename__ = "lessons"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    chapter_id: Mapped[int] = mapped_column(ForeignKey("chapters.id", ondelete="CASCADE"), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    type: Mapped[LessonType] = mapped_column(Enum(LessonType), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    duration: Mapped[int] = mapped_column(default=0, nullable=False)
    is_free: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    sort_order: Mapped[int] = mapped_column(default=0, nullable=False)

    chapter = relationship("Chapter", back_populates="lessons")
    progress_records = relationship("LessonProgress", back_populates="lesson")
