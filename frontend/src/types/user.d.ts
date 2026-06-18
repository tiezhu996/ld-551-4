import type { UserRole } from '@/constants/enums'

export interface User {
  id: number
  email: string
  name: string
  role: UserRole
  bio?: string
}

export interface LoginPayload {
  email: string
  password: string
}

export interface AuthToken {
  access_token: string
  token_type: string
  user: User
}
