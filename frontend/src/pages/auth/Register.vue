<template>
  <section class="auth-page">
    <el-card>
      <h1>注册账号</h1>
      <el-form @submit.prevent>
        <el-form-item label="姓名"><el-input v-model="form.name" /></el-form-item>
        <el-form-item label="邮箱"><el-input v-model="form.email" /></el-form-item>
        <el-form-item label="密码"><el-input v-model="form.password" type="password" show-password /></el-form-item>
        <el-form-item label="角色">
          <el-select v-model="form.role">
            <el-option label="学员" :value="UserRole.STUDENT" />
            <el-option label="讲师" :value="UserRole.INSTRUCTOR" />
          </el-select>
        </el-form-item>
        <el-button type="primary" class="wide" @click="submit">注册</el-button>
      </el-form>
    </el-card>
  </section>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import { UserRole } from '@/constants/enums'
import { useAuthStore } from '@/stores/authStore'

const router = useRouter()
const auth = useAuthStore()
const form = reactive({ name: '', email: '', password: '', role: UserRole.STUDENT })

async function submit() {
  await auth.register(form)
  router.push('/courses')
}
</script>

<style scoped>
.auth-page {
  min-height: 70vh;
  display: grid;
  place-items: center;
}

.wide {
  width: 100%;
}
</style>
