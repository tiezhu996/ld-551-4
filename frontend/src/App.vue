<template>
  <el-container class="app-shell">
    <el-header class="topbar">
      <RouterLink class="brand" to="/courses">EduFlow</RouterLink>
      <nav>
        <RouterLink to="/courses">课程</RouterLink>
        <RouterLink to="/dashboard">仪表盘</RouterLink>
        <RouterLink v-permission="[UserRole.INSTRUCTOR, UserRole.ADMIN]" to="/instructor/courses">讲师管理</RouterLink>
      </nav>
      <div class="account">
        <span v-if="auth.user">{{ auth.user.name }} · {{ auth.user.role }}</span>
        <el-button v-if="auth.user" text @click="auth.logout()">退出</el-button>
        <el-button v-else type="primary" @click="$router.push('/login')">登录</el-button>
      </div>
    </el-header>
    <el-main>
      <RouterView />
    </el-main>
  </el-container>
</template>

<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import { UserRole } from '@/constants/enums'
import { useAuthStore } from '@/stores/authStore'

const auth = useAuthStore()
</script>
