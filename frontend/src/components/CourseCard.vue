<template>
  <el-card class="course-card" shadow="hover">
    <img class="cover" :src="course.cover_image" :alt="course.title" />
    <div class="body">
      <div class="tags">
        <el-tag size="small">{{ course.category }}</el-tag>
        <el-tag size="small" type="success">{{ courseLevelLabel[course.level] }}</el-tag>
        <el-tag v-if="showStatus" size="small" type="info">{{ courseStatusLabel[course.status] }}</el-tag>
      </div>
      <h3>{{ course.title }}</h3>
      <p>{{ course.description }}</p>
      <div class="meta">
        <span>{{ course.instructor?.name || '讲师' }}</span>
        <span>{{ course.total_lessons }} 课时</span>
        <span>评分 {{ course.rating.toFixed(1) }}</span>
      </div>
      <ProgressIndicator v-if="progress !== undefined" :percentage="progress" compact />
      <div class="footer">
        <strong>{{ formatMoney(course.price) }}</strong>
        <el-button type="primary" size="small" @click="$router.push(`/courses/${course.id}`)">查看</el-button>
      </div>
    </div>
  </el-card>
</template>

<script setup lang="ts">
import { courseLevelLabel, courseStatusLabel } from '@/constants/enums'
import type { Course } from '@/types/course'
import { formatMoney } from '@/utils/format'
import ProgressIndicator from '@/components/ProgressIndicator.vue'

defineProps<{
  course: Course
  progress?: number
  showStatus?: boolean
}>()
</script>

<style scoped>
.course-card {
  overflow: hidden;
}

.cover {
  width: 100%;
  aspect-ratio: 16 / 9;
  object-fit: cover;
  display: block;
}

.body {
  display: grid;
  gap: 12px;
}

.tags,
.meta,
.footer {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

h3 {
  margin: 0;
  font-size: 18px;
}

p {
  margin: 0;
  color: #5f6673;
  min-height: 42px;
}

.meta {
  color: #6b7280;
  font-size: 13px;
}

.footer {
  justify-content: space-between;
}
</style>
