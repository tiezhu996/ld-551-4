from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Chapter(Base):
    __tablename__ = "chapters"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    sort_order: Mapped[int] = mapped_column(default=0, nullable=False)

    course = relationship("Course", back_populates="chapters")
    lessons = relationship("Lesson", back_populates="chapter", cascade="all, delete-orphan", order_by="Lesson.sort_order")
