import type { Lesson } from '@/types/lesson'

export interface Chapter {
  id: number
  course_id: number
  title: string
  sort_order: number
  lessons: Lesson[]
}
