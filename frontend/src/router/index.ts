import { createRouter, createWebHistory } from 'vue-router'
import { UserRole } from '@/constants/enums'
import { setupRouterGuards } from '@/router/guards'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', redirect: '/courses' },
    { path: '/courses', component: () => import('@/pages/courses/CourseList.vue') },
    { path: '/courses/:id', component: () => import('@/pages/courses/CourseDetail.vue') },
    { path: '/learn/:courseId', component: () => import('@/pages/learn/LearnPage.vue'), meta: { requiresAuth: true, roles: [UserRole.STUDENT, UserRole.ADMIN] } },
    { path: '/dashboard', component: () => import('@/pages/Dashboard.vue'), meta: { requiresAuth: true, roles: [UserRole.STUDENT, UserRole.ADMIN] } },
    { path: '/instructor/courses', component: () => import('@/pages/instructor/Courses.vue'), meta: { requiresAuth: true, roles: [UserRole.INSTRUCTOR, UserRole.ADMIN] } },
    { path: '/login', component: () => import('@/pages/auth/Login.vue') },
    { path: '/register', component: () => import('@/pages/auth/Register.vue') },
    { path: '/403', component: { template: '<main class="empty-page"><h1>403</h1><p>无权限访问</p></main>' } }
  ]
})

setupRouterGuards(router)

export default router
