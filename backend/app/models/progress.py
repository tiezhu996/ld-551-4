from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class LessonProgress(Base):
    __tablename__ = "lesson_progress"
    __table_args__ = (UniqueConstraint("enrollment_id", "lesson_id", name="uq_progress_enrollment_lesson"),)

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    enrollment_id: Mapped[int] = mapped_column(ForeignKey("enrollments.id", ondelete="CASCADE"), nullable=False)
    lesson_id: Mapped[int] = mapped_column(ForeignKey("lessons.id"), nullable=False)
    completed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    score: Mapped[int | None] = mapped_column(nullable=True)

    enrollment = relationship("Enrollment", back_populates="lesson_progress")
    lesson = relationship("Lesson", back_populates="progress_records")
