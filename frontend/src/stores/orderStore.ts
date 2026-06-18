import { defineStore } from 'pinia'
import { ref } from 'vue'
import { OrderStatus } from '@/constants/enums'
import type { Order } from '@/types/order'
import request from '@/utils/request'

export const useOrderStore = defineStore('order', () => {
  const currentOrder = ref<Order | null>(null)

  async function createOrder(courseId: number) {
    currentOrder.value = await request.post<unknown, Order>('/orders', { course_id: courseId, payment_method: 'mock' })
    return currentOrder.value
  }

  async function payOrder(orderId: number) {
    const order = await request.post<unknown, Order>(`/orders/${orderId}/pay`, { payment_method: 'mock' })
    if (order.status === OrderStatus.PAID) currentOrder.value = order
    return order
  }

  async function refund(orderId: number) {
    currentOrder.value = await request.post<unknown, Order>(`/orders/${orderId}/refund`)
    return currentOrder.value
  }

  return { currentOrder, createOrder, payOrder, refund }
})
