import type { App, DirectiveBinding } from 'vue'
import { UserRole } from '@/constants/enums'
import { useAuthStore } from '@/stores/authStore'

function hasPermission(roles: UserRole[]): boolean {
  const auth = useAuthStore()
  return !!auth.user && roles.includes(auth.user.role)
}

export default {
  install(app: App) {
    app.directive('permission', {
      mounted(el: HTMLElement, binding: DirectiveBinding<UserRole[]>) {
        if (!hasPermission(binding.value)) el.remove()
      }
    })
  }
}
