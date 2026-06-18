from datetime import UTC, datetime, timedelta
from decimal import Decimal
from uuid import uuid4

from sqlalchemy.orm import Session

from app.constants.enums import CourseStatus, OrderStatus
from app.exceptions.course import CourseNotFoundException
from app.exceptions.payment import InvalidOrderTransitionException, PaymentFailedException
from app.models.course import Course
from app.models.coupon import CouponUsage
from app.models.enrollment import Enrollment
from app.models.order import Order
from app.models.user import User
from app.services.audit_service import AuditService
from app.services.coupon_service import CouponService
from app.services.enrollment_service import EnrollmentService


class PaymentService:
    @staticmethod
    def create_order(
        db: Session,
        user: User,
        course_id: int,
        payment_method: str = "mock",
        coupon_code: str | None = None,
        ip_address: str | None = None,
    ) -> Order:
        course = db.get(Course, course_id)
        if not course or course.status != CourseStatus.PUBLISHED:
            raise CourseNotFoundException("课程不存在或未上架")
        if db.query(Enrollment).filter_by(user_id=user.id, course_id=course_id).first():
            raise PaymentFailedException("已注册该课程")

        original_amount = course.price
        discount_amount = Decimal("0")
        coupon_id = None
        applied_coupon_code = None

        if coupon_code:
            valid, message, discount = CouponService.validate_coupon(db, coupon_code, course, user)
            if not valid:
                raise PaymentFailedException(message or "优惠券不可用")
            coupon = CouponService.get_coupon_by_code(db, coupon_code)
            if coupon and discount is not None:
                coupon_id = coupon.id
                discount_amount = discount
                applied_coupon_code = coupon.code

        final_amount = (original_amount - discount_amount).quantize(Decimal("0.01"))
        if final_amount < Decimal("0"):
            final_amount = Decimal("0")

        order = Order(
            order_no=f"EF{datetime.now(UTC):%Y%m%d%H%M%S}{uuid4().hex[:8].upper()}",
            user_id=user.id,
            course_id=course_id,
            amount=final_amount,
            original_amount=original_amount,
            coupon_id=coupon_id,
            discount_amount=discount_amount,
            coupon_code=applied_coupon_code,
            payment_method=payment_method,
            status=OrderStatus.PENDING,
        )
        db.add(order)
        db.flush()

        after_data = {
            "course_id": course_id,
            "original_amount": str(original_amount),
            "discount_amount": str(discount_amount),
            "amount": str(final_amount),
            "coupon_code": applied_coupon_code or "",
        }
        AuditService.record(
            db,
            user_id=user.id,
            action="CREATE",
            entity="Order",
            entity_id=str(order.id),
            after_data=after_data,
            ip_address=ip_address,
        )
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

        if order.coupon_id:
            CouponService.apply_coupon(db, order.coupon_id, user.id, order.id, order.discount_amount)

        order.status = OrderStatus.PAID
        order.payment_method = payment_info.get("payment_method", order.payment_method)
        order.paid_at = datetime.now(UTC)
        EnrollmentService.enroll(db, user, order.course, ip_address=ip_address)
        AuditService.record(
            db,
            user_id=user.id,
            action="UPDATE",
            entity="Order",
            entity_id=str(order.id),
            before_data={"status": OrderStatus.PENDING.value},
            after_data={"status": OrderStatus.PAID.value},
            ip_address=ip_address,
        )
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

        if order.coupon_id:
            usage = db.query(CouponUsage).filter(
                CouponUsage.coupon_id == order.coupon_id,
                CouponUsage.order_id == order.id,
            ).first()
            if usage:
                from app.models.coupon import Coupon
                coupon = db.get(Coupon, order.coupon_id)
                if coupon and coupon.used_quantity > 0:
                    coupon.used_quantity -= 1
                db.delete(usage)

        enrollment = db.query(Enrollment).filter_by(user_id=order.user_id, course_id=order.course_id).first()
        if enrollment:
            db.delete(enrollment)
            order.course.student_count = max(order.course.student_count - 1, 0)
        order.status = OrderStatus.REFUNDED
        AuditService.record(
            db,
            user_id=user.id,
            action="UPDATE",
            entity="Order",
            entity_id=str(order.id),
            before_data={"status": OrderStatus.PAID.value},
            after_data={"status": OrderStatus.REFUNDED.value},
            ip_address=ip_address,
        )
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
        AuditService.record(
            db,
            user_id=user.id,
            action="UPDATE",
            entity="Order",
            entity_id=str(order.id),
            before_data={"status": OrderStatus.PENDING.value},
            after_data={"status": OrderStatus.CANCELLED.value},
            ip_address=ip_address,
        )
        db.commit()
        db.refresh(order)
        return order
