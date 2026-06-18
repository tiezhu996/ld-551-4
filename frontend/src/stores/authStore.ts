import { defineStore } from 'pinia'
import { computed, ref } from 'vue'
import { UserRole } from '@/constants/enums'
import type { AuthToken, LoginPayload, User } from '@/types/user'
import request from '@/utils/request'
import { clearToken, setToken } from '@/utils/auth'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(localStorage.getItem('eduflow_token'))
  const role = computed(() => user.value?.role)
  const isInstructor = computed(() => role.value === UserRole.INSTRUCTOR || role.value === UserRole.ADMIN)

  async function login(payload: LoginPayload) {
    const data = await request.post<unknown, AuthToken>('/auth/login', payload)
    token.value = data.access_token
    user.value = data.user
    setToken(data.access_token)
  }

  async function register(payload: LoginPayload & { name: string; role?: UserRole }) {
    const data = await request.post<unknown, AuthToken>('/auth/register', payload)
    token.value = data.access_token
    user.value = data.user
    setToken(data.access_token)
  }

  async function fetchMe() {
    if (!token.value) return
    user.value = await request.get<unknown, User>('/auth/me')
  }

  function logout() {
    user.value = null
    token.value = null
    clearToken()
  }

  return { user, token, role, isInstructor, login, register, fetchMe, logout }
})
