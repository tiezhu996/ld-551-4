# EduFlow 在线课程学习平台

EduFlow 是一个前后端分离的在线课程学习平台，覆盖课程发布、学员注册、在线学习、进度跟踪、订单支付、讲师管理、RBAC 权限与审计日志。

## 功能

- 学员：浏览课程、购买/注册课程、学习视频/文本/测验课时、查看学习进度与仪表盘。
- 讲师：创建课程、管理课程状态、查看课程学生数据入口。
- 管理员：审核上架课程、跨角色权限管理基础能力。
- 支付：Mock 支付服务，支持 `PENDING -> PAID -> REFUNDED` 和 `PENDING -> CANCELLED` 状态流转，重复支付回调幂等处理。
- 横切能力：JWT 认证、RBAC、数据范围过滤、统一异常响应、写操作审计日志。

## 快速启动 Docker Compose

```bash
cp .env.example .env
docker compose up --build
```

访问地址：

- 前端：http://localhost:38401
- 后端：http://localhost:38501
- 健康检查：http://localhost:38501/health

演示账号默认密码均为 `password`：

- 管理员：`admin@eduflow.example.com`
- 讲师：`instructor@eduflow.example.com`
- 学员：`student@eduflow.example.com`

## 本地开发

后端：

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
DATABASE_URL=sqlite:///./dev.db uvicorn app.main:app --host 0.0.0.0 --port 38501
```

前端：

```bash
cd frontend
npm install
npm run dev
```

## 技术栈

| 层级 | 技术 |
|---|---|
| 前端 | Vue 3、TypeScript、Vite、Element Plus、Pinia、Axios、Vue Router |
| 后端 | FastAPI、SQLAlchemy 2、Pydantic、JWT、Passlib |
| 数据 | PostgreSQL、Redis |
| 部署 | Docker Compose、Nginx 反向代理 |

## 目录结构

```text
backend/      FastAPI API、模型、Schema、Service、中间件
frontend/     Vue 3 页面、组件、Store、路由、请求封装
database/     PostgreSQL 初始化脚本与种子数据
docker-compose.yml
.env.example
```

## 环境变量

| 变量 | 说明 | 默认值 |
|---|---|---|
| `COMPOSE_PROJECT_NAME` | Compose 容器名前缀 | `ldeduflow` |
| `DATABASE_URL` | 后端数据库连接 | `postgresql+psycopg://eduflow:eduflow@postgres:5432/eduflow` |
| `REDIS_URL` | Redis 连接 | `redis://redis:6379/0` |
| `JWT_SECRET_KEY` | JWT 签名密钥 | `please-change-this-secret` |
| `FRONTEND_PORT` | 前端端口 | `38401` |
| `BACKEND_PORT` | 后端端口 | `38501` |
| `POSTGRES_PORT` | PostgreSQL 宿主机端口 | `54321` |
| `REDIS_PORT` | Redis 宿主机端口 | `63791` |

## 共享枚举使用位置

1. `backend/app/constants/enums.py` — 后端枚举定义
2. `frontend/src/constants/enums.ts` — 前端枚举定义
3. `backend/app/models/course.py` — Course 模型引用 CourseStatus、CourseLevel
4. `backend/app/models/lesson.py` — Lesson 模型引用 LessonType
5. `backend/app/models/order.py` — Order 模型引用 OrderStatus
6. `backend/app/models/user.py` — User 模型引用 UserRole
7. `backend/app/services/payment_service.py` — 支付服务引用 OrderStatus
8. `backend/app/api/deps.py` — 认证依赖引用 UserRole
9. `backend/app/middleware/error_handler.py` — 异常处理中引用枚举
10. `frontend/src/types/course.d.ts` — 课程类型引用 CourseStatus、CourseLevel、LessonType
11. `frontend/src/types/order.d.ts` — 订单类型引用 OrderStatus
12. `frontend/src/stores/authStore.ts` — 认证 store 引用 UserRole
13. `frontend/src/stores/courseStore.ts` — 课程 store 引用 CourseStatus
14. `frontend/src/stores/orderStore.ts` — 订单 store 引用 OrderStatus
15. `frontend/src/components/CourseCard.vue` — 展示课程状态和难度标签
16. `frontend/src/router/guards.ts` — 路由守卫引用 UserRole
17. `frontend/src/pages/instructor/Courses.vue` — 讲师管理页引用 CourseStatus

## Docker 说明

- `docker-compose.yml` 顶层使用 `name: ldeduflow`，未使用废弃 `version` 字段。
- 前端 Nginx 监听容器 80 端口，并将 `/api` 反向代理到 `backend:38501`。
- PostgreSQL 使用命名卷 `postgres_data` 持久化。
- PostgreSQL、Redis、Backend 均配置健康检查，服务按健康状态依赖启动。
- 所有可变配置通过 `.env` 注入，目录名包含中文也不影响 Compose 相对路径解析。

## License

MIT
