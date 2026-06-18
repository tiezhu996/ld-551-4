import type { OrderStatus } from '@/constants/enums'

export interface Order {
  id: number
  order_no: string
  user_id: number
  course_id: number
  amount: string | number
  payment_method: string
  status: OrderStatus
  paid_at?: string
  created_at: string
  updated_at: string
}
