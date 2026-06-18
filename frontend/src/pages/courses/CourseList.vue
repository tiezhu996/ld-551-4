<template>
  <section class="page course-list">
    <aside class="filters">
      <h2>筛选</h2>
      <el-input v-model="query.keyword" clearable placeholder="搜索标题或描述" @keyup.enter="load" />
      <el-select v-model="query.category" clearable placeholder="分类">
        <el-option label="编程" value="编程" />
        <el-option label="设计" value="设计" />
        <el-option label="商业" value="商业" />
      </el-select>
      <el-select v-model="query.level" clearable placeholder="难度">
        <el-option label="入门" :value="CourseLevel.BEGINNER" />
        <el-option label="进阶" :value="CourseLevel.INTERMEDIATE" />
        <el-option label="高级" :value="CourseLevel.ADVANCED" />
      </el-select>
      <el-radio-group v-model="query.sort">
        <el-radio-button value="latest">最新</el-radio-button>
        <el-radio-button value="hot">最热</el-radio-button>
        <el-radio-button value="rating">评分</el-radio-button>
      </el-radio-group>
      <el-button type="primary" @click="load">应用筛选</el-button>
    </aside>
    <main>
      <div class="page-title">
        <h1>已上架课程</h1>
        <span>{{ courseStore.total }} 门课程</span>
      </div>
      <div class="grid">
        <CourseCard v-for="course in courseStore.courses" :key="course.id" :course="course" />
      </div>
    </main>
  </section>
</template>

<script setup lang="ts">
import { onMounted, reactive, watch } from 'vue'
import CourseCard from '@/components/CourseCard.vue'
import { CourseLevel } from '@/constants/enums'
import { useCourseStore } from '@/stores/courseStore'
import type { CourseQuery } from '@/types/course'

const courseStore = useCourseStore()
const query = reactive<CourseQuery>({ keyword: '', category: '', level: '', sort: 'latest', page: 1, size: 12 })

function load() {
  courseStore.fetchCourses(query)
}

watch(() => query.sort, load)
onMounted(load)
</script>

<style scoped>
.course-list {
  display: grid;
  grid-template-columns: 260px 1fr;
  gap: 24px;
}

.filters {
  display: grid;
  align-content: start;
  gap: 14px;
  padding: 18px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  background: #fff;
}
</style>
