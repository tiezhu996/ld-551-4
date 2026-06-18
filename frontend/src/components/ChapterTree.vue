<template>
  <el-tree
    class="chapter-tree"
    :data="treeData"
    node-key="key"
    default-expand-all
    draggable
    :allow-drop="allowDrop"
    @node-click="handleClick"
  >
    <template #default="{ data }">
      <span class="tree-node">
        <span>{{ data.label }}</span>
        <el-tag v-if="data.lesson?.is_free" size="small">试看</el-tag>
      </span>
    </template>
  </el-tree>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { Chapter } from '@/types/chapter'
import type { Lesson } from '@/types/lesson'

const props = defineProps<{ chapters: Chapter[] }>()
const emit = defineEmits<{ selectLesson: [lesson: Lesson] }>()

const treeData = computed(() =>
  props.chapters.map((chapter) => ({
    key: `chapter-${chapter.id}`,
    label: `${chapter.sort_order}. ${chapter.title}`,
    children: chapter.lessons.map((lesson) => ({
      key: `lesson-${lesson.id}`,
      label: `${lesson.sort_order}. ${lesson.title} · ${lesson.duration}分钟`,
      lesson
    }))
  }))
)

function allowDrop() {
  return true
}

function handleClick(data: { lesson?: Lesson }) {
  if (data.lesson) emit('selectLesson', data.lesson)
}
</script>

<style scoped>
.chapter-tree {
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 8px;
}

.tree-node {
  width: 100%;
  display: flex;
  justify-content: space-between;
  gap: 8px;
}
</style>
