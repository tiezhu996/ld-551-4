from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field

from app.constants.enums import CouponType, CouponStatus


class CouponCreate(BaseModel):
    code: str = Field(..., max_length=50)
    name: str = Field(..., max_length=120)
    type: CouponType
    value: Decimal
    min_amount: Decimal = Decimal("0")
    max_discount: Decimal | None = None
    total_quantity: int = -1
    per_user_limit: int = 1
    valid_from: datetime
    valid_until: datetime
    description: str | None = None
    course_ids: list[int] = []


class CouponUpdate(BaseModel):
    name: str | None = None
    type: CouponType | None = None
    value: Decimal | None = None
    min_amount: Decimal | None = None
    max_discount: Decimal | None = None
    total_quantity: int | None = None
    per_user_limit: int | None = None
    valid_from: datetime | None = None
    valid_until: datetime | None = None
    description: str | None = None
    course_ids: list[int] | None = None


class CouponStatusUpdate(BaseModel):
    status: CouponStatus


class CouponResponse(BaseModel):
    id: int
    code: str
    name: str
    type: CouponType
    value: Decimal
    min_amount: Decimal
    max_discount: Decimal | None
    total_quantity: int
    used_quantity: int
    per_user_limit: int
    valid_from: datetime
    valid_until: datetime
    status: CouponStatus
    description: str | None
    course_ids: list[int] = []
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class CouponValidateRequest(BaseModel):
    code: str
    course_id: int


class CouponValidateResponse(BaseModel):
    valid: bool
    coupon: CouponResponse | None = None
    discount_amount: Decimal | None = None
    final_amount: Decimal | None = None
    message: str | None = None


class CouponApplyRequest(BaseModel):
    code: str
