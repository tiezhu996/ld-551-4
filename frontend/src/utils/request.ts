import axios from 'axios'
import { ElMessage } from 'element-plus'
import router from '@/router'
import { clearToken, getToken } from '@/utils/auth'

const request = axios.create({
  baseURL: '/api',
  timeout: 10000
})

request.interceptors.request.use((config) => {
  const token = getToken()
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

request.interceptors.response.use(
  (response) => response.data,
  (error) => {
    if (!error.response) {
      ElMessage.error('网络连接异常')
      return Promise.reject(error)
    }
    const status = error.response.status
    if (status === 401) {
      clearToken()
      router.push('/login')
    } else if (status === 403) {
      ElMessage.error('无权限访问')
    } else if (status === 404) {
      ElMessage.error('资源不存在')
    } else if (status >= 500) {
      ElMessage.error('服务器错误，请稍后重试')
    } else {
      ElMessage.error(error.response.data?.message || '请求失败')
    }
    return Promise.reject(error)
  }
)

export default request
