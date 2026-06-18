from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Enum, ForeignKey, Numeric, String, Integer, UniqueConstraint, func, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.constants.enums import CouponType, CouponStatus
from app.core.database import Base


class Coupon(Base):
    __tablename__ = "coupons"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    code: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    type: Mapped[CouponType] = mapped_column(Enum(CouponType), nullable=False)
    value: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    min_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=0, nullable=False)
    max_discount: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    total_quantity: Mapped[int] = mapped_column(Integer, default=-1, nullable=False)
    used_quantity: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    per_user_limit: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    valid_from: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    valid_until: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[CouponStatus] = mapped_column(Enum(CouponStatus), default=CouponStatus.ACTIVE, nullable=False)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    coupon_courses = relationship("CouponCourse", back_populates="coupon", cascade="all, delete-orphan")
    coupon_usages = relationship("CouponUsage", back_populates="coupon", cascade="all, delete-orphan")


class CouponCourse(Base):
    __tablename__ = "coupon_courses"
    __table_args__ = (UniqueConstraint("coupon_id", "course_id", name="uq_coupon_course"),)

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    coupon_id: Mapped[int] = mapped_column(ForeignKey("coupons.id", ondelete="CASCADE"), nullable=False)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)

    coupon = relationship("Coupon", back_populates="coupon_courses")
    course = relationship("Course")


class CouponUsage(Base):
    __tablename__ = "coupon_usages"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    coupon_id: Mapped[int] = mapped_column(ForeignKey("coupons.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), nullable=False)
    discount_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    used_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    coupon = relationship("Coupon", back_populates="coupon_usages")
    user = relationship("User")
    order = relationship("Order")
