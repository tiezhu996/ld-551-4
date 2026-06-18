<template>
  <div class="progress-indicator" :class="{ compact }">
    <el-progress v-if="type === 'circle'" type="circle" :percentage="rounded" :width="compact ? 72 : 96" />
    <el-progress v-else :percentage="rounded" :stroke-width="compact ? 8 : 12" />
    <span v-if="label" class="progress-label">{{ label }}</span>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  percentage: number
  type?: 'line' | 'circle'
  label?: string
  compact?: boolean
}>()

const rounded = computed(() => Math.max(0, Math.min(100, Math.round(props.percentage || 0))))
</script>

<style scoped>
.progress-indicator {
  display: grid;
  gap: 8px;
  align-items: center;
}

.progress-label {
  color: #4b5563;
  font-size: 13px;
}

.compact {
  gap: 4px;
}
</style>
