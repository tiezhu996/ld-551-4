import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Coupon, CouponValidateResult, CouponCreatePayload, CouponUpdatePayload } from '@/types/coupon'
import type { CouponStatus } from '@/constants/enums'
import request from '@/utils/request'

export const useCouponStore = defineStore('coupon', () => {
  const coupons = ref<Coupon[]>([])
  const total = ref(0)
  const currentCoupon = ref<Coupon | null>(null)
  const validateResult = ref<CouponValidateResult | null>(null)

  const couponTypeLabel: Record<string, string> = {
    FIXED: '固定金额',
    PERCENTAGE: '折扣比例'
  }

  const couponStatusLabel: Record<string, string> = {
    ACTIVE: '启用中',
    INACTIVE: '已停用',
    EXPIRED: '已过期'
  }

  const couponStatusType: Record<string, string> = {
    ACTIVE: 'success',
    INACTIVE: 'info',
    EXPIRED: 'danger'
  }

  async function fetchCoupons(params?: { status?: CouponStatus; page?: number; size?: number }) {
    const res = await request.get<unknown, { items: Coupon[]; total: number; page: number; size: number }>('/coupons', { params })
    coupons.value = res.items
    total.value = res.total
    return res
  }

  async function fetchCoupon(id: number) {
    currentCoupon.value = await request.get<unknown, Coupon>(`/coupons/${id}`)
    return currentCoupon.value
  }

  async function createCoupon(payload: CouponCreatePayload) {
    const coupon = await request.post<unknown, Coupon>('/coupons', payload)
    return coupon
  }

  async function updateCoupon(id: number, payload: CouponUpdatePayload) {
    const coupon = await request.put<unknown, Coupon>(`/coupons/${id}`, payload)
    return coupon
  }

  async function updateCouponStatus(id: number, status: CouponStatus) {
    const coupon = await request.patch<unknown, Coupon>(`/coupons/${id}/status`, { status })
    return coupon
  }

  async function validateCoupon(code: string, courseId: number) {
    const result = await request.post<unknown, CouponValidateResult>('/coupons/validate', {
      code,
      course_id: courseId
    })
    validateResult.value = result
    return result
  }

  function formatCouponValue(coupon: Coupon): string {
    if (coupon.type === 'FIXED') {
      return `¥${coupon.value}`
    } else {
      return `${coupon.value}% OFF`
    }
  }

  return {
    coupons,
    total,
    currentCoupon,
    validateResult,
    couponTypeLabel,
    couponStatusLabel,
    couponStatusType,
    fetchCoupons,
    fetchCoupon,
    createCoupon,
    updateCoupon,
    updateCouponStatus,
    validateCoupon,
    formatCouponValue
  }
})
