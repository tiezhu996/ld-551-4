from datetime import UTC, datetime
from decimal import Decimal

from sqlalchemy.orm import Session

from app.constants.enums import CouponStatus, CouponType, CourseStatus
from app.exceptions.course import CourseNotFoundException
from app.exceptions.payment import PaymentFailedException
from app.models.coupon import Coupon, CouponCourse, CouponUsage
from app.models.course import Course
from app.models.user import User
from app.schemas.coupon import CouponCreate, CouponUpdate


class CouponService:
    @staticmethod
    def create_coupon(db: Session, data: CouponCreate) -> Coupon:
        existing = db.query(Coupon).filter(Coupon.code == data.code.upper()).first()
        if existing:
            raise PaymentFailedException("优惠券码已存在")

        coupon = Coupon(
            code=data.code.upper(),
            name=data.name,
            type=data.type,
            value=data.value,
            min_amount=data.min_amount,
            max_discount=data.max_discount,
            total_quantity=data.total_quantity,
            per_user_limit=data.per_user_limit,
            valid_from=data.valid_from,
            valid_until=data.valid_until,
            description=data.description,
            status=CouponStatus.ACTIVE,
        )
        db.add(coupon)
        db.flush()

        if data.course_ids:
            for course_id in data.course_ids:
                course = db.get(Course, course_id)
                if not course:
                    raise CourseNotFoundException(f"课程 {course_id} 不存在")
                db.add(CouponCourse(coupon_id=coupon.id, course_id=course_id))

        db.commit()
        db.refresh(coupon)
        return coupon

    @staticmethod
    def update_coupon(db: Session, coupon_id: int, data: CouponUpdate) -> Coupon:
        coupon = db.get(Coupon, coupon_id)
        if not coupon:
            raise PaymentFailedException("优惠券不存在")

        update_data = data.model_dump(exclude_unset=True)
        course_ids = update_data.pop("course_ids", None)

        for field, value in update_data.items():
            setattr(coupon, field, value)

        if course_ids is not None:
            db.query(CouponCourse).filter(CouponCourse.coupon_id == coupon_id).delete()
            for course_id in course_ids:
                course = db.get(Course, course_id)
                if not course:
                    raise CourseNotFoundException(f"课程 {course_id} 不存在")
                db.add(CouponCourse(coupon_id=coupon.id, course_id=course_id))

        db.commit()
        db.refresh(coupon)
        return coupon

    @staticmethod
    def update_status(db: Session, coupon_id: int, status: CouponStatus) -> Coupon:
        coupon = db.get(Coupon, coupon_id)
        if not coupon:
            raise PaymentFailedException("优惠券不存在")
        coupon.status = status
        db.commit()
        db.refresh(coupon)
        return coupon

    @staticmethod
    def get_coupon(db: Session, coupon_id: int) -> Coupon | None:
        return db.get(Coupon, coupon_id)

    @staticmethod
    def get_coupon_by_code(db: Session, code: str) -> Coupon | None:
        return db.query(Coupon).filter(Coupon.code == code.upper()).first()

    @staticmethod
    def list_coupons(db: Session, status: CouponStatus | None = None, skip: int = 0, limit: int = 20) -> tuple[list[Coupon], int]:
        query = db.query(Coupon)
        if status:
            query = query.filter(Coupon.status == status)
        total = query.count()
        coupons = query.order_by(Coupon.id.desc()).offset(skip).limit(limit).all()
        return coupons, total

    @staticmethod
    def get_coupon_course_ids(db: Session, coupon_id: int) -> list[int]:
        rows = db.query(CouponCourse.course_id).filter(CouponCourse.coupon_id == coupon_id).all()
        return [row[0] for row in rows]

    @staticmethod
    def calculate_discount(coupon: Coupon, original_amount: Decimal) -> Decimal:
        if coupon.type == CouponType.FIXED:
            discount = coupon.value
        else:
            discount = original_amount * coupon.value / Decimal("100")
            if coupon.max_discount and discount > coupon.max_discount:
                discount = coupon.max_discount

        if discount > original_amount:
            discount = original_amount

        return discount.quantize(Decimal("0.01"))

    @staticmethod
    def validate_coupon(db: Session, code: str, course: Course, user: User) -> tuple[bool, str, Decimal | None]:
        coupon = CouponService.get_coupon_by_code(db, code)
        if not coupon:
            return False, "优惠券不存在", None

        now = datetime.now(UTC)
        if coupon.status != CouponStatus.ACTIVE:
            return False, "优惠券不可用", None

        if coupon.valid_from.replace(tzinfo=UTC) > now:
            return False, "优惠券尚未生效", None

        if coupon.valid_until.replace(tzinfo=UTC) < now:
            return False, "优惠券已过期", None

        if course.status != CourseStatus.PUBLISHED:
            return False, "课程未上架", None

        course_ids = CouponService.get_coupon_course_ids(db, coupon.id)
        if course_ids and course.id not in course_ids:
            return False, "该优惠券不适用于此课程", None

        if course.price < coupon.min_amount:
            return False, f"订单金额需满 {coupon.min_amount} 元才可使用", None

        if coupon.total_quantity != -1 and coupon.used_quantity >= coupon.total_quantity:
            return False, "优惠券已被领完", None

        user_usage_count = db.query(CouponUsage).filter(
            CouponUsage.coupon_id == coupon.id,
            CouponUsage.user_id == user.id,
        ).count()
        if user_usage_count >= coupon.per_user_limit:
            return False, "您已达到该优惠券的使用上限", None

        discount = CouponService.calculate_discount(coupon, course.price)
        return True, "优惠券可用", discount

    @staticmethod
    def apply_coupon(db: Session, coupon_id: int, user_id: int, order_id: int, discount_amount: Decimal) -> None:
        usage = CouponUsage(
            coupon_id=coupon_id,
            user_id=user_id,
            order_id=order_id,
            discount_amount=discount_amount,
        )
        db.add(usage)

        coupon = db.get(Coupon, coupon_id)
        if coupon:
            coupon.used_quantity += 1

    @staticmethod
    def build_coupon_response(db: Session, coupon: Coupon) -> dict:
        course_ids = CouponService.get_coupon_course_ids(db, coupon.id)
        result = {c.name: getattr(coupon, c.name) for c in coupon.__table__.columns}
        result["course_ids"] = course_ids
        return result
