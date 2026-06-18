import { defineStore } from 'pinia'
import { ref } from 'vue'
import { CourseStatus } from '@/constants/enums'
import type { Chapter } from '@/types/chapter'
import type { Course, CourseQuery } from '@/types/course'
import request from '@/utils/request'

interface PageResult<T> {
  total: number
  page: number
  size: number
  items: T[]
}

export const useCourseStore = defineStore('course', () => {
  const courses = ref<Course[]>([])
  const currentCourse = ref<Course | null>(null)
  const chapters = ref<Chapter[]>([])
  const total = ref(0)
  const loading = ref(false)

  async function fetchCourses(query: CourseQuery = {}) {
    loading.value = true
    try {
      const data = await request.get<unknown, PageResult<Course>>('/courses', { params: query })
      courses.value = data.items
      total.value = data.total
    } finally {
      loading.value = false
    }
  }

  async function fetchCourse(id: number) {
    currentCourse.value = await request.get<unknown, Course>(`/courses/${id}`)
    chapters.value = currentCourse.value.chapters || []
  }

  async function fetchChapters(id: number) {
    chapters.value = await request.get<unknown, Chapter[]>(`/courses/${id}/chapters`)
  }

  async function createCourse(payload: Partial<Course>) {
    return request.post<unknown, Course>('/courses', payload)
  }

  async function updateStatus(courseId: number, status: CourseStatus) {
    return request.patch<unknown, Course>(`/courses/${courseId}/status`, { status })
  }

  return { courses, currentCourse, chapters, total, loading, fetchCourses, fetchCourse, fetchChapters, createCourse, updateStatus }
})
