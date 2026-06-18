from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel

from app.constants.enums import OrderStatus


class OrderCreate(BaseModel):
    course_id: int
    payment_method: str = "mock"


class PaymentConfirm(BaseModel):
    payment_method: str = "mock"
    callback_id: str | None = None


class OrderResponse(BaseModel):
    id: int
    order_no: str
    user_id: int
    course_id: int
    amount: Decimal
    payment_method: str
    status: OrderStatus
    paid_at: datetime | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
