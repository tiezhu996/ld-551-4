import type { Course } from '@/types/course'

export interface Enrollment {
  id: number
  user_id: number
  course_id: number
  enrolled_at: string
  progress: number
  last_access_at: string
  course?: Course
}

export interface ProgressSummary {
  enrollment_id: number
  course_id: number
  progress: number
  completed_lessons: number
  total_lessons: number
}
