import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Enrollment, ProgressSummary } from '@/types/enrollment'
import request from '@/utils/request'

export const useEnrollmentStore = defineStore('enrollment', () => {
  const enrollments = ref<Enrollment[]>([])
  const progress = ref<ProgressSummary | null>(null)

  async function fetchEnrollments() {
    enrollments.value = await request.get<unknown, Enrollment[]>('/enrollments')
  }

  async function fetchProgress(courseId: number) {
    progress.value = await request.get<unknown, ProgressSummary>(`/enrollments/${courseId}/progress`)
  }

  async function completeLesson(lessonId: number, score?: number) {
    const enrollment = await request.post<unknown, Enrollment>('/enrollments/progress/complete', { lesson_id: lessonId, score })
    await fetchProgress(enrollment.course_id)
    return enrollment
  }

  return { enrollments, progress, fetchEnrollments, fetchProgress, completeLesson }
})
