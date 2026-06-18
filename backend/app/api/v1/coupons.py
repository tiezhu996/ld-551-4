from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_role
from app.constants.enums import CouponStatus, CourseStatus, UserRole
from app.core.database import get_db
from app.exceptions.course import CourseNotFoundException
from app.models.course import Course
from app.models.user import User
from app.schemas.common import PageResponse
from app.schemas.coupon import (
    CouponCreate,
    CouponResponse,
    CouponStatusUpdate,
    CouponUpdate,
    CouponValidateRequest,
    CouponValidateResponse,
)
from app.services.coupon_service import CouponService

router = APIRouter(prefix="/coupons", tags=["coupons"])


@router.get("", response_model=PageResponse[CouponResponse])
def list_coupons(
    status: CouponStatus | None = None,
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    _: User = Depends(require_role(UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    skip = (page - 1) * size
    coupons, total = CouponService.list_coupons(db, status=status, skip=skip, limit=size)
    items = []
    for coupon in coupons:
        data = CouponService.build_coupon_response(db, coupon)
        items.append(CouponResponse(**data))
    return PageResponse(items=items, total=total, page=page, size=size)


@router.get("/{coupon_id}", response_model=CouponResponse)
def get_coupon(
    coupon_id: int,
    _: User = Depends(require_role(UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    coupon = CouponService.get_coupon(db, coupon_id)
    if not coupon:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="优惠券不存在")
    data = CouponService.build_coupon_response(db, coupon)
    return CouponResponse(**data)


@router.post("", response_model=CouponResponse)
def create_coupon(
    payload: CouponCreate,
    request: Request,
    user: User = Depends(require_role(UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    coupon = CouponService.create_coupon(db, payload)
    from app.services.audit_service import AuditService
    AuditService.record(
        db,
        user_id=user.id,
        action="CREATE",
        entity="Coupon",
        entity_id=str(coupon.id),
        after_data={"code": coupon.code, "name": coupon.name, "type": coupon.type.value},
        ip_address=request.client.host if request.client else None,
    )
    db.commit()
    data = CouponService.build_coupon_response(db, coupon)
    return CouponResponse(**data)


@router.put("/{coupon_id}", response_model=CouponResponse)
def update_coupon(
    coupon_id: int,
    payload: CouponUpdate,
    request: Request,
    user: User = Depends(require_role(UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    coupon = CouponService.update_coupon(db, coupon_id, payload)
    from app.services.audit_service import AuditService
    AuditService.record(
        db,
        user_id=user.id,
        action="UPDATE",
        entity="Coupon",
        entity_id=str(coupon.id),
        after_data=payload.model_dump(exclude_unset=True),
        ip_address=request.client.host if request.client else None,
    )
    db.commit()
    data = CouponService.build_coupon_response(db, coupon)
    return CouponResponse(**data)


@router.patch("/{coupon_id}/status", response_model=CouponResponse)
def update_coupon_status(
    coupon_id: int,
    payload: CouponStatusUpdate,
    request: Request,
    user: User = Depends(require_role(UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    coupon = CouponService.update_status(db, coupon_id, payload.status)
    from app.services.audit_service import AuditService
    AuditService.record(
        db,
        user_id=user.id,
        action="UPDATE",
        entity="Coupon",
        entity_id=str(coupon.id),
        after_data={"status": payload.status.value},
        ip_address=request.client.host if request.client else None,
    )
    db.commit()
    data = CouponService.build_coupon_response(db, coupon)
    return CouponResponse(**data)


@router.post("/validate", response_model=CouponValidateResponse)
def validate_coupon(
    payload: CouponValidateRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    course = db.get(Course, payload.course_id)
    if not course or course.status != CourseStatus.PUBLISHED:
        raise CourseNotFoundException("课程不存在或未上架")

    valid, message, discount = CouponService.validate_coupon(db, payload.code, course, user)
    coupon = CouponService.get_coupon_by_code(db, payload.code)

    response = CouponValidateResponse(valid=valid, message=message)
    if valid and coupon and discount is not None:
        coupon_data = CouponService.build_coupon_response(db, coupon)
        response.coupon = CouponResponse(**coupon_data)
        response.discount_amount = discount
        response.final_amount = (course.price - discount).quantize(__import__("decimal").Decimal("0.01"))

    return response
