import type { CouponType, CouponStatus } from '@/constants/enums'

export interface Coupon {
  id: number
  code: string
  name: string
  type: CouponType
  value: string | number
  min_amount: string | number
  max_discount: string | number | null
  total_quantity: number
  used_quantity: number
  per_user_limit: number
  valid_from: string
  valid_until: string
  status: CouponStatus
  description: string | null
  course_ids: number[]
  created_at: string
  updated_at: string
}

export interface CouponValidateResult {
  valid: boolean
  coupon: Coupon | null
  discount_amount: string | number | null
  final_amount: string | number | null
  message: string | null
}

export interface CouponCreatePayload {
  code: string
  name: string
  type: CouponType
  value: number
  min_amount: number
  max_discount?: number | null
  total_quantity: number
  per_user_limit: number
  valid_from: string
  valid_until: string
  description?: string
  course_ids: number[]
}

export interface CouponUpdatePayload {
  name?: string
  type?: CouponType
  value?: number
  min_amount?: number
  max_discount?: number | null
  total_quantity?: number
  per_user_limit?: number
  valid_from?: string
  valid_until?: string
  description?: string
  course_ids?: number[]
}
