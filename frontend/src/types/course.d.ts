import type { CourseLevel, CourseStatus, LessonType } from '@/constants/enums'
import type { Chapter } from '@/types/chapter'
import type { User } from '@/types/user'

export interface Course {
  id: number
  title: string
  description: string
  instructor_id: number
  instructor?: User
  category: string
  level: CourseLevel
  price: string | number
  cover_image: string
  total_lessons: number
  total_duration: number
  status: CourseStatus
  rating: number
  student_count: number
  created_at: string
  updated_at: string
  chapters?: Chapter[]
}

export interface CourseQuery {
  category?: string
  level?: CourseLevel | ''
  keyword?: string
  sort?: 'latest' | 'hot' | 'rating'
  page?: number
  size?: number
}

export interface LessonPreview {
  type: LessonType
  title: string
}
