<template>
  <section class="page">
    <div class="page-header">
      <h2>优惠券管理</h2>
      <el-button type="primary" @click="openCreateDialog">创建优惠券</el-button>
    </div>

    <el-card>
      <el-form :inline="true" @submit.prevent>
        <el-form-item label="状态">
          <el-select v-model="filterStatus" placeholder="全部" clearable style="width: 140px" @change="fetchCoupons">
            <el-option label="启用中" value="ACTIVE" />
            <el-option label="已停用" value="INACTIVE" />
            <el-option label="已过期" value="EXPIRED" />
          </el-select>
        </el-form-item>
      </el-form>

      <el-table :data="couponStore.coupons" v-loading="loading">
        <el-table-column prop="code" label="券码" width="140" />
        <el-table-column prop="name" label="名称" min-width="160" />
        <el-table-column label="类型" width="100">
          <template #default="{ row }">{{ couponStore.couponTypeLabel[row.type] }}</template>
        </el-table-column>
        <el-table-column label="面值/折扣" width="120">
          <template #default="{ row }">
            <span class="discount-value">{{ couponStore.formatCouponValue(row) }}</span>
          </template>
        </el-table-column>
        <el-table-column label="使用门槛" width="120">
          <template #default="{ row }">
            <span v-if="Number(row.min_amount) > 0">满 {{ row.min_amount }} 元</span>
            <span v-else>无门槛</span>
          </template>
        </el-table-column>
        <el-table-column label="有效期" min-width="220">
          <template #default="{ row }">
            <div class="valid-period">
              <div>{{ formatDate(row.valid_from) }}</div>
              <div class="arrow">→</div>
              <div>{{ formatDate(row.valid_until) }}</div>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="使用情况" width="140">
          <template #default="{ row }">
            <span>{{ row.used_quantity }} / {{ row.total_quantity === -1 ? '不限' : row.total_quantity }}</span>
          </template>
        </el-table-column>
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="couponStore.couponStatusType[row.status]">
              {{ couponStore.couponStatusLabel[row.status] }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" @click="openEditDialog(row)">编辑</el-button>
            <el-button
              v-if="row.status === 'ACTIVE'"
              link
              type="warning"
              @click="toggleStatus(row, 'INACTIVE')"
            >停用</el-button>
            <el-button
              v-else-if="row.status === 'INACTIVE'"
              link
              type="success"
              @click="toggleStatus(row, 'ACTIVE')"
            >启用</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
        v-model:current-page="page"
        v-model:page-size="size"
        :total="couponStore.total"
        :page-sizes="[10, 20, 50, 100]"
        layout="total, sizes, prev, pager, next, jumper"
        class="pagination"
        @current-change="fetchCoupons"
        @size-change="fetchCoupons"
      />
    </el-card>

    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑优惠券' : '创建优惠券'"
      width="640px"
      @close="resetForm"
    >
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px">
        <el-form-item label="券码" prop="code">
          <el-input v-model="form.code" placeholder="请输入优惠券码，如 NEWYEAR2024" :disabled="isEdit" maxlength="50" />
        </el-form-item>
        <el-form-item label="名称" prop="name">
          <el-input v-model="form.name" placeholder="优惠券名称" maxlength="120" />
        </el-form-item>
        <el-form-item label="类型" prop="type">
          <el-radio-group v-model="form.type">
            <el-radio value="FIXED">固定金额</el-radio>
            <el-radio value="PERCENTAGE">折扣比例</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="面值" prop="value">
          <el-input-number v-model="form.value" :min="0" :precision="2" />
          <span class="unit-tip" v-if="form.type === 'FIXED'">元</span>
          <span class="unit-tip" v-else>% 折扣</span>
        </el-form-item>
        <el-form-item label="最低消费" prop="min_amount">
          <el-input-number v-model="form.min_amount" :min="0" :precision="2" />
          <span class="unit-tip">元</span>
        </el-form-item>
        <el-form-item v-if="form.type === 'PERCENTAGE'" label="最高抵扣" prop="max_discount">
          <el-input-number v-model="form.max_discount" :min="0" :precision="2" :controls="false" placeholder="不限制则留空" />
          <span class="unit-tip">元</span>
        </el-form-item>
        <el-form-item label="总数量" prop="total_quantity">
          <el-input-number v-model="form.total_quantity" :min="-1" />
          <span class="unit-tip">张（-1 表示不限）</span>
        </el-form-item>
        <el-form-item label="每人限领" prop="per_user_limit">
          <el-input-number v-model="form.per_user_limit" :min="1" />
          <span class="unit-tip">张</span>
        </el-form-item>
        <el-form-item label="有效期" prop="valid_period">
          <el-date-picker
            v-model="form.valid_period"
            type="datetimerange"
            range-separator="至"
            start-placeholder="开始时间"
            end-placeholder="结束时间"
            value-format="YYYY-MM-DDTHH:mm:ss"
          />
        </el-form-item>
        <el-form-item label="适用课程" prop="course_ids">
          <el-select v-model="form.course_ids" multiple placeholder="不选则全部课程可用" style="width: 100%">
            <el-option
              v-for="course in courseList"
              :key="course.id"
              :label="course.title"
              :value="course.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input v-model="form.description" type="textarea" :rows="2" placeholder="选填" maxlength="500" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>
  </section>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus'
import { useCouponStore } from '@/stores/couponStore'
import { useCourseStore } from '@/stores/courseStore'
import { CouponType, CouponStatus } from '@/constants/enums'
import type { Coupon } from '@/types/coupon'

const couponStore = useCouponStore()
const courseStore = useCourseStore()

const loading = ref(false)
const submitting = ref(false)
const dialogVisible = ref(false)
const isEdit = ref(false)
const editingId = ref<number | null>(null)
const filterStatus = ref<CouponStatus | ''>('')
const page = ref(1)
const size = ref(20)
const formRef = ref<FormInstance>()
const courseList = ref<Array<{ id: number; title: string }>>([])

interface CouponForm {
  code: string
  name: string
  type: CouponType
  value: number
  min_amount: number
  max_discount: number | null
  total_quantity: number
  per_user_limit: number
  valid_period: [string, string] | null
  course_ids: number[]
  description: string
}

const form = reactive<CouponForm>({
  code: '',
  name: '',
  type: CouponType.FIXED,
  value: 0,
  min_amount: 0,
  max_discount: null,
  total_quantity: -1,
  per_user_limit: 1,
  valid_period: null,
  course_ids: [],
  description: ''
})

const rules: FormRules = {
  code: [{ required: true, message: '请输入优惠券码', trigger: 'blur' }],
  name: [{ required: true, message: '请输入优惠券名称', trigger: 'blur' }],
  type: [{ required: true, message: '请选择类型', trigger: 'change' }],
  value: [{ required: true, message: '请输入面值', trigger: 'blur' }],
  valid_period: [{ required: true, message: '请选择有效期', trigger: 'change' }]
}

async function fetchCoupons() {
  loading.value = true
  try {
    await couponStore.fetchCoupons({
      status: filterStatus.value || undefined,
      page: page.value,
      size: size.value
    })
  } finally {
    loading.value = false
  }
}

async function fetchCourses() {
  try {
    const res = await courseStore.fetchCourses({ page: 1, size: 100 })
    courseList.value = (res as unknown as { items: Array<{ id: number; title: string }> }).items
  } catch {
    // ignore
  }
}

function resetForm() {
  form.code = ''
  form.name = ''
  form.type = CouponType.FIXED
  form.value = 0
  form.min_amount = 0
  form.max_discount = null
  form.total_quantity = -1
  form.per_user_limit = 1
  form.valid_period = null
  form.course_ids = []
  form.description = ''
  isEdit.value = false
  editingId.value = null
  formRef.value?.clearValidate()
}

function openCreateDialog() {
  resetForm()
  dialogVisible.value = true
}

function openEditDialog(row: Coupon) {
  isEdit.value = true
  editingId.value = row.id
  form.code = row.code
  form.name = row.name
  form.type = row.type
  form.value = Number(row.value)
  form.min_amount = Number(row.min_amount)
  form.max_discount = row.max_discount ? Number(row.max_discount) : null
  form.total_quantity = row.total_quantity
  form.per_user_limit = row.per_user_limit
  form.valid_period = [row.valid_from, row.valid_until]
  form.course_ids = [...row.course_ids]
  form.description = row.description || ''
  dialogVisible.value = true
}

async function handleSubmit() {
  if (!formRef.value) return
  await formRef.value.validate(async (valid) => {
    if (!valid || !form.valid_period) return
    submitting.value = true
    try {
      const payload = {
        code: form.code,
        name: form.name,
        type: form.type,
        value: form.value,
        min_amount: form.min_amount,
        max_discount: form.max_discount,
        total_quantity: form.total_quantity,
        per_user_limit: form.per_user_limit,
        valid_from: form.valid_period[0],
        valid_until: form.valid_period[1],
        description: form.description || undefined,
        course_ids: form.course_ids
      }
      if (isEdit.value && editingId.value) {
        await couponStore.updateCoupon(editingId.value, payload)
        ElMessage.success('更新成功')
      } else {
        await couponStore.createCoupon(payload)
        ElMessage.success('创建成功')
      }
      dialogVisible.value = false
      fetchCoupons()
    } finally {
      submitting.value = false
    }
  })
}

async function toggleStatus(row: Coupon, status: CouponStatus) {
  const actionText = status === CouponStatus.ACTIVE ? '启用' : '停用'
  try {
    await ElMessageBox.confirm(`确定${actionText}优惠券「${row.name}」吗？`, '提示', {
      type: 'warning'
    })
  } catch {
    return
  }
  try {
    await couponStore.updateCouponStatus(row.id, status)
    ElMessage.success(`${actionText}成功`)
    fetchCoupons()
  } catch {
    // error handled globally
  }
}

function formatDate(dateStr: string): string {
  const d = new Date(dateStr)
  return d.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(() => {
  fetchCoupons()
  fetchCourses()
})
</script>

<style scoped>
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.page-header h2 {
  margin: 0;
  font-size: 20px;
}

.discount-value {
  color: #f56c6c;
  font-weight: 600;
}

.valid-period {
  display: flex;
  flex-direction: column;
  gap: 4px;
  font-size: 13px;
}

.valid-period .arrow {
  display: none;
}

.unit-tip {
  margin-left: 8px;
  color: #909399;
  font-size: 13px;
}

.pagination {
  margin-top: 16px;
  justify-content: flex-end;
}
</style>
