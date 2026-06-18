<template>
  <section class="page" v-if="course">
    <div class="detail-head">
      <img :src="course.cover_image" :alt="course.title" />
      <div>
        <el-tag>{{ course.category }}</el-tag>
        <h1>{{ course.title }}</h1>
        <p>{{ course.description }}</p>
        <div class="detail-meta">
          <span>{{ course.instructor?.name }}</span>
          <span>{{ formatMinutes(course.total_duration) }}</span>
          <span>评分 {{ course.rating }}</span>
        </div>
        <div class="price-section">
          <div class="price-main">
            <span class="current-price" v-if="validCoupon">
              {{ formatMoney(validateResult?.final_amount || course.price) }}
            </span>
            <span class="original-price" v-if="validCoupon">
              {{ formatMoney(course.price) }}
            </span>
            <span class="current-price" v-else>{{ formatMoney(course.price) }}</span>
          </div>
          <div class="discount-tag" v-if="validCoupon">
            <el-tag type="danger">{{ validateResult?.coupon?.name }}</el-tag>
            <span class="discount-amount">-{{ formatMoney(validateResult?.discount_amount || 0) }}</span>
          </div>
        </div>
        <div class="coupon-input" v-if="Number(course.price) > 0">
          <el-input
            v-model="couponCode"
            placeholder="输入优惠券码"
            class="coupon-input-field"
            @keyup.enter="applyCoupon"
          />
          <el-button type="primary" :disabled="!couponCode.trim()" @click="applyCoupon">
            验证
          </el-button>
          <el-button v-if="validCoupon" text type="danger" @click="clearCoupon">
            不使用
          </el-button>
        </div>
        <div class="coupon-message" v-if="couponMessage">
          <el-tag :type="validCoupon ? 'success' : 'danger'" effect="plain">
            {{ couponMessage }}
          </el-tag>
        </div>
        <div class="actions">
          <el-button type="primary" size="large" @click="buy">立即购买</el-button>
          <el-button size="large" @click="$router.push(`/learn/${course.id}`)">继续学习</el-button>
        </div>
      </div>
    </div>
    <el-tabs>
      <el-tab-pane label="大纲">
        <ChapterTree :chapters="chapters" />
      </el-tab-pane>
      <el-tab-pane label="介绍">
        <article class="rich-text">{{ course.description }}</article>
      </el-tab-pane>
      <el-tab-pane label="评价">
        <el-empty description="评价模块预留，评分已在课程卡片展示" />
      </el-tab-pane>
    </el-tabs>
  </section>
</template>

<script setup lang="ts">
import { computed, ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import ChapterTree from '@/components/ChapterTree.vue'
import { useCourseStore } from '@/stores/courseStore'
import { useOrderStore } from '@/stores/orderStore'
import { useCouponStore } from '@/stores/couponStore'
import { formatMinutes, formatMoney } from '@/utils/format'
import { useAuthStore } from '@/stores/authStore'

const route = useRoute()
const router = useRouter()
const courseStore = useCourseStore()
const orderStore = useOrderStore()
const couponStore = useCouponStore()
const authStore = useAuthStore()

const course = computed(() => courseStore.currentCourse)
const chapters = computed(() => courseStore.chapters)

const couponCode = ref('')
const validCoupon = ref(false)
const couponMessage = ref('')
const validateResult = computed(() => couponStore.validateResult)

async function applyCoupon() {
  if (!course.value || !couponCode.value.trim()) return
  if (!authStore.token) {
    ElMessage.warning('请先登录')
    router.push('/login')
    return
  }
  try {
    const result = await couponStore.validateCoupon(couponCode.value.trim(), course.value.id)
    validCoupon.value = result.valid
    couponMessage.value = result.message || ''
  } catch (e: unknown) {
    validCoupon.value = false
    couponMessage.value = (e as { message?: string })?.message || '验证失败'
  }
}

function clearCoupon() {
  couponCode.value = ''
  validCoupon.value = false
  couponMessage.value = ''
  couponStore.validateResult = null
}

async function buy() {
  if (!course.value) return
  if (Number(course.value.price) === 0) {
    ElMessage.success('免费课程可直接进入学习')
    router.push(`/learn/${course.value.id}`)
    return
  }
  const code = validCoupon.value ? couponCode.value.trim() : undefined
  const order = await orderStore.createOrder(course.value.id, code)
  await orderStore.payOrder(order.id)
  ElMessage.success('支付成功，已注册课程')
  router.push(`/learn/${course.value.id}`)
}

onMounted(() => courseStore.fetchCourse(Number(route.params.id)))
</script>

<style scoped>
.detail-head {
  display: grid;
  grid-template-columns: 420px 1fr;
  gap: 28px;
  padding: 20px;
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  margin-bottom: 20px;
}

.detail-head img {
  width: 100%;
  aspect-ratio: 16 / 10;
  object-fit: cover;
  border-radius: 8px;
}

.detail-meta,
.actions {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.price-section {
  margin: 16px 0;
}

.price-main {
  display: flex;
  align-items: baseline;
  gap: 12px;
}

.current-price {
  font-size: 32px;
  font-weight: 700;
  color: #b45309;
}

.original-price {
  font-size: 18px;
  color: #9ca3af;
  text-decoration: line-through;
}

.discount-tag {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 8px;
}

.discount-amount {
  color: #f56c6c;
  font-weight: 600;
  font-size: 14px;
}

.coupon-input {
  display: flex;
  gap: 10px;
  align-items: center;
  margin-bottom: 12px;
}

.coupon-input-field {
  width: 240px;
}

.coupon-message {
  margin-bottom: 12px;
}

.rich-text {
  line-height: 1.8;
  background: #fff;
  padding: 18px;
  border-radius: 8px;
}
</style>
