<template>
  <section class="page learn-page">
    <LessonPlayer :lesson="selectedLesson" @complete="complete" />
    <aside class="learn-side">
      <ProgressIndicator :percentage="progress?.progress || 0" type="circle" label="学习进度" />
      <ChapterTree :chapters="chapters" @select-lesson="selectedLesson = $event" />
      <el-input v-model="note" type="textarea" :rows="6" placeholder="学习笔记" />
    </aside>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import ChapterTree from '@/components/ChapterTree.vue'
import LessonPlayer from '@/components/LessonPlayer.vue'
import ProgressIndicator from '@/components/ProgressIndicator.vue'
import { useCourseStore } from '@/stores/courseStore'
import { useEnrollmentStore } from '@/stores/enrollmentStore'
import type { Lesson } from '@/types/lesson'

const route = useRoute()
const courseStore = useCourseStore()
const enrollmentStore = useEnrollmentStore()
const selectedLesson = ref<Lesson | null>(null)
const note = ref('')
const chapters = computed(() => courseStore.chapters)
const progress = computed(() => enrollmentStore.progress)

async function complete(score?: number) {
  if (selectedLesson.value) await enrollmentStore.completeLesson(selectedLesson.value.id, score)
}

onMounted(async () => {
  const courseId = Number(route.params.courseId)
  await courseStore.fetchCourse(courseId)
  selectedLesson.value = courseStore.chapters[0]?.lessons[0] || null
  await enrollmentStore.fetchProgress(courseId)
})
</script>

<style scoped>
.learn-page {
  display: grid;
  grid-template-columns: minmax(0, 7fr) minmax(300px, 3fr);
  gap: 20px;
}

.learn-side {
  display: grid;
  gap: 16px;
  align-content: start;
}
</style>
