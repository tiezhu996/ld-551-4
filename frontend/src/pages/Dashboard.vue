<template>
  <section class="page">
    <div class="page-title">
      <h1>学习仪表盘</h1>
    </div>
    <div class="stats">
      <el-statistic title="已注册课程" :value="enrollments.length" />
      <el-statistic title="总学习进度" :value="averageProgress" suffix="%" />
      <el-statistic title="已完成课程" :value="completedCount" />
    </div>
    <h2>我的课程</h2>
    <div class="grid">
      <CourseCard v-for="item in enrollments" :key="item.id" :course="item.course!" :progress="item.progress" />
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import CourseCard from '@/components/CourseCard.vue'
import { useEnrollmentStore } from '@/stores/enrollmentStore'

const store = useEnrollmentStore()
const enrollments = computed(() => store.enrollments)
const averageProgress = computed(() => {
  if (!enrollments.value.length) return 0
  return Math.round(enrollments.value.reduce((sum, item) => sum + item.progress, 0) / enrollments.value.length)
})
const completedCount = computed(() => enrollments.value.filter((item) => item.progress >= 100).length)

onMounted(store.fetchEnrollments)
</script>

<style scoped>
.stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}

.stats :deep(.el-statistic) {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 18px;
}
</style>
