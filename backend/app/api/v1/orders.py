from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.order import OrderCreate, OrderResponse, PaymentConfirm
from app.services.payment_service import PaymentService

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("", response_model=OrderResponse)
def create_order(payload: OrderCreate, request: Request, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return PaymentService.create_order(db, user, payload.course_id, payload.payment_method, request.client.host if request.client else None)


@router.post("/{order_id}/pay", response_model=OrderResponse)
def pay_order(order_id: int, payload: PaymentConfirm, request: Request, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return PaymentService.process_payment(db, user, order_id, payload.model_dump(), request.client.host if request.client else None)


@router.post("/{order_id}/refund", response_model=OrderResponse)
def refund_order(order_id: int, request: Request, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return PaymentService.refund(db, user, order_id, request.client.host if request.client else None)


@router.post("/{order_id}/cancel", response_model=OrderResponse)
def cancel_order(order_id: int, request: Request, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return PaymentService.cancel(db, user, order_id, request.client.host if request.client else None)
