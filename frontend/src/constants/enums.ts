export enum CourseStatus {
  DRAFT = 'DRAFT',
  PUBLISHED = 'PUBLISHED',
  ARCHIVED = 'ARCHIVED'
}

export enum CourseLevel {
  BEGINNER = 'BEGINNER',
  INTERMEDIATE = 'INTERMEDIATE',
  ADVANCED = 'ADVANCED'
}

export enum LessonType {
  VIDEO = 'VIDEO',
  TEXT = 'TEXT',
  QUIZ = 'QUIZ'
}

export enum OrderStatus {
  PENDING = 'PENDING',
  PAID = 'PAID',
  REFUNDED = 'REFUNDED',
  CANCELLED = 'CANCELLED'
}

export enum UserRole {
  STUDENT = 'STUDENT',
  INSTRUCTOR = 'INSTRUCTOR',
  ADMIN = 'ADMIN'
}

export const courseLevelLabel: Record<CourseLevel, string> = {
  [CourseLevel.BEGINNER]: '入门',
  [CourseLevel.INTERMEDIATE]: '进阶',
  [CourseLevel.ADVANCED]: '高级'
}

export const courseStatusLabel: Record<CourseStatus, string> = {
  [CourseStatus.DRAFT]: '草稿',
  [CourseStatus.PUBLISHED]: '已上架',
  [CourseStatus.ARCHIVED]: '已归档'
}
