from datetime import UTC, datetime, timedelta
from uuid import uuid4

from sqlalchemy.orm import Session

from app.constants.enums import CourseStatus, OrderStatus
from app.exceptions.course import CourseNotFoundException
from app.exceptions.payment import InvalidOrderTransitionException, PaymentFailedException
from app.models.course import Course
from app.models.enrollment import Enrollment
from app.models.order import Order
from app.models.user import User
from app.services.audit_service import AuditService
from app.services.enrollment_service import EnrollmentService


class PaymentService:
    @staticmethod
    def create_order(db: Session, user: User, course_id: int, payment_method: str = "mock", ip_address: str | None = None) -> Order:
        course = db.get(Course, course_id)
        if not course or course.status != CourseStatus.PUBLISHED:
            raise CourseNotFoundException("课程不存在或未上架")
        if db.query(Enrollment).filter_by(user_id=user.id, course_id=course_id).first():
            raise PaymentFailedException("已注册该课程")
        order = Order(
            order_no=f"EF{datetime.now(UTC):%Y%m%d%H%M%S}{uuid4().hex[:8].upper()}",
            user_id=user.id,
            course_id=course_id,
            amount=course.price,
            payment_method=payment_method,
            status=OrderStatus.PENDING,
        )
        db.add(order)
        db.flush()
        AuditService.record(db, user_id=user.id, action="CREATE", entity="Order", entity_id=str(order.id), after_data={"course_id": course_id, "amount": str(course.price)}, ip_address=ip_address)
        db.commit()
        db.refresh(order)
        return order

    @staticmethod
    def process_payment(db: Session, user: User, order_id: int, payment_info: dict, ip_address: str | None = None) -> Order:
        order = db.get(Order, order_id)
        if not order or order.user_id != user.id:
            raise PaymentFailedException("订单不存在")
        if order.status == OrderStatus.PAID:
            return order
        if order.status != OrderStatus.PENDING:
            raise InvalidOrderTransitionException()
        if order.created_at and order.created_at.replace(tzinfo=UTC) < datetime.now(UTC) - timedelta(minutes=30):
            order.status = OrderStatus.CANCELLED
            db.commit()
            raise InvalidOrderTransitionException("订单已超时取消")
        order.status = OrderStatus.PAID
        order.payment_method = payment_info.get("payment_method", order.payment_method)
        order.paid_at = datetime.now(UTC)
        EnrollmentService.enroll(db, user, order.course, ip_address=ip_address)
        AuditService.record(db, user_id=user.id, action="UPDATE", entity="Order", entity_id=str(order.id), before_data={"status": OrderStatus.PENDING.value}, after_data={"status": OrderStatus.PAID.value}, ip_address=ip_address)
        db.commit()
        db.refresh(order)
        return order

    @staticmethod
    def refund(db: Session, user: User, order_id: int, ip_address: str | None = None) -> Order:
        order = db.get(Order, order_id)
        if not order or order.user_id != user.id:
            raise PaymentFailedException("订单不存在")
        if order.status != OrderStatus.PAID:
            raise InvalidOrderTransitionException()
        enrollment = db.query(Enrollment).filter_by(user_id=order.user_id, course_id=order.course_id).first()
        if enrollment:
            db.delete(enrollment)
            order.course.student_count = max(order.course.student_count - 1, 0)
        order.status = OrderStatus.REFUNDED
        AuditService.record(db, user_id=user.id, action="UPDATE", entity="Order", entity_id=str(order.id), before_data={"status": OrderStatus.PAID.value}, after_data={"status": OrderStatus.REFUNDED.value}, ip_address=ip_address)
        db.commit()
        db.refresh(order)
        return order

    @staticmethod
    def cancel(db: Session, user: User, order_id: int, ip_address: str | None = None) -> Order:
        order = db.get(Order, order_id)
        if not order or order.user_id != user.id:
            raise PaymentFailedException("订单不存在")
        if order.status != OrderStatus.PENDING:
            raise InvalidOrderTransitionException()
        order.status = OrderStatus.CANCELLED
        AuditService.record(db, user_id=user.id, action="UPDATE", entity="Order", entity_id=str(order.id), before_data={"status": OrderStatus.PENDING.value}, after_data={"status": OrderStatus.CANCELLED.value}, ip_address=ip_address)
        db.commit()
        db.refresh(order)
        return order
