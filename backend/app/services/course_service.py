from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload

from app.constants.enums import CourseStatus, UserRole
from app.exceptions.course import CourseNotFoundException, CoursePermissionException
from app.models.chapter import Chapter
from app.models.course import Course
from app.models.lesson import Lesson
from app.models.user import User
from app.schemas.course import CourseCreate, CourseUpdate
from app.services.audit_service import AuditService


class CourseService:
    @staticmethod
    def list_published(
        db: Session,
        *,
        category: str | None = None,
        level: str | None = None,
        keyword: str | None = None,
        sort: str = "latest",
        page: int = 1,
        size: int = 12,
    ) -> tuple[int, list[Course]]:
        query = db.query(Course).options(joinedload(Course.instructor)).filter(Course.status == CourseStatus.PUBLISHED)
        if category:
            query = query.filter(Course.category == category)
        if level:
            query = query.filter(Course.level == level)
        if keyword:
            pattern = f"%{keyword}%"
            query = query.filter(or_(Course.title.ilike(pattern), Course.description.ilike(pattern)))
        if sort == "hot":
            query = query.order_by(Course.student_count.desc(), Course.created_at.desc())
        elif sort == "rating":
            query = query.order_by(Course.rating.desc(), Course.created_at.desc())
        else:
            query = query.order_by(Course.created_at.desc())
        total = query.count()
        return total, query.offset((page - 1) * size).limit(size).all()

    @staticmethod
    def get_course(db: Session, course_id: int) -> Course:
        course = (
            db.query(Course)
            .options(joinedload(Course.instructor), joinedload(Course.chapters).joinedload(Chapter.lessons))
            .filter(Course.id == course_id)
            .first()
        )
        if not course:
            raise CourseNotFoundException()
        return course

    @staticmethod
    def create_course(db: Session, instructor: User, payload: CourseCreate, ip_address: str | None = None) -> Course:
        course = Course(**payload.model_dump(), instructor_id=instructor.id, status=CourseStatus.DRAFT)
        db.add(course)
        db.flush()
        AuditService.record(db, user_id=instructor.id, action="CREATE", entity="Course", entity_id=str(course.id), after_data={"title": course.title}, ip_address=ip_address)
        db.commit()
        db.refresh(course)
        return course

    @staticmethod
    def update_course(db: Session, user: User, course_id: int, payload: CourseUpdate, ip_address: str | None = None) -> Course:
        course = CourseService.get_course(db, course_id)
        if user.role != UserRole.ADMIN and course.instructor_id != user.id:
            raise CoursePermissionException()
        before = {"title": course.title, "status": course.status.value}
        for key, value in payload.model_dump(exclude_unset=True).items():
            setattr(course, key, value)
        AuditService.record(db, user_id=user.id, action="UPDATE", entity="Course", entity_id=str(course.id), before_data=before, after_data=payload.model_dump(exclude_unset=True), ip_address=ip_address)
        db.commit()
        db.refresh(course)
        return course

    @staticmethod
    def change_status(db: Session, user: User, course_id: int, status: CourseStatus, ip_address: str | None = None) -> Course:
        course = CourseService.get_course(db, course_id)
        if user.role != UserRole.ADMIN and course.instructor_id != user.id:
            raise CoursePermissionException()
        before = {"status": course.status.value}
        if course.status == CourseStatus.DRAFT and status == CourseStatus.PUBLISHED and user.role != UserRole.ADMIN:
            raise CoursePermissionException("课程上架需要管理员审核")
        course.status = status
        AuditService.record(db, user_id=user.id, action="UPDATE", entity="Course", entity_id=str(course.id), before_data=before, after_data={"status": status.value}, ip_address=ip_address)
        db.commit()
        db.refresh(course)
        return course

    @staticmethod
    def instructor_courses(db: Session, instructor: User) -> list[Course]:
        return db.query(Course).filter(Course.instructor_id == instructor.id).order_by(Course.updated_at.desc()).all()

    @staticmethod
    def recalculate_course_stats(db: Session, course_id: int) -> None:
        lessons = db.query(Lesson).join(Chapter).filter(Chapter.course_id == course_id).all()
        course = db.get(Course, course_id)
        if course:
            course.total_lessons = len(lessons)
            course.total_duration = sum(lesson.duration for lesson in lessons)
