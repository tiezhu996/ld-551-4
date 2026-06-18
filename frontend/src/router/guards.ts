import type { Router } from 'vue-router'
import { UserRole } from '@/constants/enums'
import { useAuthStore } from '@/stores/authStore'

export function setupRouterGuards(router: Router) {
  router.beforeEach(async (to) => {
    const auth = useAuthStore()
    if (auth.token && !auth.user) {
      try {
        await auth.fetchMe()
      } catch {
        auth.logout()
      }
    }
    if (to.meta.requiresAuth && !auth.user) return '/login'
    const roles = to.meta.roles as UserRole[] | undefined
    if (roles?.length && (!auth.user || !roles.includes(auth.user.role))) return '/403'
    return true
  })
}
