<template>
  <section class="lesson-player">
    <template v-if="lesson">
      <header>
        <h2>{{ lesson.title }}</h2>
        <el-tag>{{ lesson.type }}</el-tag>
      </header>
      <video v-if="lesson.type === LessonType.VIDEO" controls class="video" @ended="complete">
        <source :src="lesson.content" />
      </video>
      <article v-else-if="lesson.type === LessonType.TEXT" class="text-content" @scroll.passive="handleScroll">
        {{ lesson.content }}
      </article>
      <el-form v-else class="quiz" @submit.prevent>
        <el-form-item label="答案">
          <el-input v-model="answer" placeholder="请输入测验答案" />
        </el-form-item>
        <el-button type="primary" @click="submitQuiz">提交测验</el-button>
      </el-form>
      <el-button class="complete" type="success" plain @click="complete">标记完成</el-button>
    </template>
    <el-empty v-else description="请选择课时" />
  </section>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { LessonType } from '@/constants/enums'
import type { Lesson } from '@/types/lesson'

defineProps<{ lesson: Lesson | null }>()
const emit = defineEmits<{ complete: [score?: number] }>()
const answer = ref('')

function complete() {
  emit('complete')
}

function submitQuiz() {
  emit('complete', answer.value.trim() ? 100 : 0)
}

function handleScroll(event: Event) {
  const el = event.target as HTMLElement
  if (el.scrollTop + el.clientHeight >= el.scrollHeight - 8) complete()
}
</script>

<style scoped>
.lesson-player {
  min-height: 520px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 20px;
  background: #fff;
}

header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
}

.video {
  width: 100%;
  aspect-ratio: 16 / 9;
  background: #111827;
  border-radius: 8px;
}

.text-content {
  height: 360px;
  overflow-y: auto;
  white-space: pre-wrap;
  line-height: 1.8;
  color: #374151;
}

.complete {
  margin-top: 16px;
}
</style>
