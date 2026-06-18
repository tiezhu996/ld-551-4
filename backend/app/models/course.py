from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Enum, ForeignKey, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.constants.enums import CourseLevel, CourseStatus
from app.core.database import Base


class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), index=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    instructor_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    category: Mapped[str] = mapped_column(String(80), index=True, nullable=False)
    level: Mapped[CourseLevel] = mapped_column(Enum(CourseLevel), nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=0, nullable=False)
    cover_image: Mapped[str] = mapped_column(String(500), nullable=False)
    total_lessons: Mapped[int] = mapped_column(default=0, nullable=False)
    total_duration: Mapped[int] = mapped_column(default=0, nullable=False)
    status: Mapped[CourseStatus] = mapped_column(Enum(CourseStatus), default=CourseStatus.DRAFT, nullable=False)
    rating: Mapped[float] = mapped_column(default=0, nullable=False)
    student_count: Mapped[int] = mapped_column(default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    instructor = relationship("User", back_populates="courses")
    chapters = relationship("Chapter", back_populates="course", cascade="all, delete-orphan", order_by="Chapter.sort_order")
    enrollments = relationship("Enrollment", back_populates="course", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="course", cascade="all, delete-orphan")
