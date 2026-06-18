<template>
  <section class="auth-page">
    <el-card>
      <h1>登录 EduFlow</h1>
      <el-form @submit.prevent>
        <el-form-item label="邮箱"><el-input v-model="form.email" /></el-form-item>
        <el-form-item label="密码"><el-input v-model="form.password" type="password" show-password /></el-form-item>
        <el-button type="primary" class="wide" @click="submit">登录</el-button>
      </el-form>
      <RouterLink to="/register">创建账号</RouterLink>
    </el-card>
  </section>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import { useRouter, RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'

const router = useRouter()
const auth = useAuthStore()
const form = reactive({ email: 'student@eduflow.example.com', password: 'password' })

async function submit() {
  await auth.login(form)
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
