from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Enum, ForeignKey, Numeric, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.constants.enums import OrderStatus
from app.core.database import Base


class Order(Base):
    __tablename__ = "orders"
    __table_args__ = (UniqueConstraint("order_no", name="uq_order_no"),)

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    order_no: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"), nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    payment_method: Mapped[str] = mapped_column(String(30), default="mock", nullable=False)
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus), default=OrderStatus.PENDING, nullable=False)
    paid_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="orders")
    course = relationship("Course", back_populates="orders")
