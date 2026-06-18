import type { OrderStatus } from '@/constants/enums'

export interface Order {
  id: number
  order_no: string
  user_id: number
  course_id: number
  amount: string | number
  original_amount: string | number
  coupon_id: number | null
  discount_amount: string | number
  coupon_code: string | null
  payment_method: string
  status: OrderStatus
  paid_at?: string
  created_at: string
  updated_at: string
}
