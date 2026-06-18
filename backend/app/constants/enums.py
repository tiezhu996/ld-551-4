from enum import StrEnum


class CourseStatus(StrEnum):
    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"
    ARCHIVED = "ARCHIVED"


class CourseLevel(StrEnum):
    BEGINNER = "BEGINNER"
    INTERMEDIATE = "INTERMEDIATE"
    ADVANCED = "ADVANCED"


class LessonType(StrEnum):
    VIDEO = "VIDEO"
    TEXT = "TEXT"
    QUIZ = "QUIZ"


class OrderStatus(StrEnum):
    PENDING = "PENDING"
    PAID = "PAID"
    REFUNDED = "REFUNDED"
    CANCELLED = "CANCELLED"


class UserRole(StrEnum):
    STUDENT = "STUDENT"
    INSTRUCTOR = "INSTRUCTOR"
    ADMIN = "ADMIN"
