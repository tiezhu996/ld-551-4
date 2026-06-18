<template>
  <section class="page">
    <div class="page-title">
      <h1>讲师课程管理</h1>
      <el-button type="primary" @click="dialogVisible = true">创建课程</el-button>
    </div>
    <el-table :data="rows" border>
      <el-table-column prop="title" label="课程" min-width="220" />
      <el-table-column prop="category" label="分类" width="100" />
      <el-table-column label="状态" width="120">
        <template #default="{ row }">
          <el-tag>{{ courseStatusLabel[row.status as CourseStatus] }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="student_count" label="学员" width="90" />
      <el-table-column prop="rating" label="评分" width="90" />
      <el-table-column label="操作" width="220">
        <template #default="{ row }">
          <el-button size="small">编辑</el-button>
          <el-button size="small" @click="archive(row.id)">下架</el-button>
          <el-button size="small" type="primary">学生数据</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="dialogVisible" title="创建课程" width="520">
      <el-form label-width="88px">
        <el-form-item label="标题"><el-input v-model="form.title" /></el-form-item>
        <el-form-item label="分类"><el-input v-model="form.category" /></el-form-item>
        <el-form-item label="难度">
          <el-select v-model="form.level">
            <el-option label="入门" :value="CourseLevel.BEGINNER" />
            <el-option label="进阶" :value="CourseLevel.INTERMEDIATE" />
            <el-option label="高级" :value="CourseLevel.ADVANCED" />
          </el-select>
        </el-form-item>
        <el-form-item label="价格"><el-input-number v-model="form.price" :min="0" /></el-form-item>
        <el-form-item label="封面"><el-input v-model="form.cover_image" /></el-form-item>
        <el-form-item label="描述"><el-input v-model="form.description" type="textarea" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="create">保存</el-button>
      </template>
    </el-dialog>
  </section>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import request from '@/utils/request'
import { CourseLevel, CourseStatus, courseStatusLabel } from '@/constants/enums'
import { useCourseStore } from '@/stores/courseStore'
import type { Course } from '@/types/course'

const courseStore = useCourseStore()
const rows = ref<Course[]>([])
const dialogVisible = ref(false)
const form = reactive({
  title: '',
  description: '',
  category: '编程',
  level: CourseLevel.BEGINNER,
  price: 0,
  cover_image: 'https://images.unsplash.com/photo-1516321318423-f06f85e504b3'
})

async function load() {
  rows.value = await request.get<unknown, Course[]>('/instructor/courses')
}

async function create() {
  await courseStore.createCourse(form)
  dialogVisible.value = false
  await load()
}

async function archive(id: number) {
  await courseStore.updateStatus(id, CourseStatus.ARCHIVED)
  await load()
}

onMounted(load)
</script>
