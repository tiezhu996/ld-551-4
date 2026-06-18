INSERT INTO users (id, email, name, hashed_password, role, bio) VALUES
  (1, 'admin@eduflow.example.com', '平台管理员', '$2a$12$uXW/0qc.ZntzytbhEbVTmeZcnwlQugDgbcig.FUyhnoNRCrtGXLHC', 'ADMIN', '负责课程审核与平台运营'),
  (2, 'instructor@eduflow.example.com', '林老师', '$2a$12$uXW/0qc.ZntzytbhEbVTmeZcnwlQugDgbcig.FUyhnoNRCrtGXLHC', 'INSTRUCTOR', '十年全栈开发与教学经验'),
  (3, 'student@eduflow.example.com', '体验学员', '$2a$12$uXW/0qc.ZntzytbhEbVTmeZcnwlQugDgbcig.FUyhnoNRCrtGXLHC', 'STUDENT', '正在学习 Vue 与 FastAPI')
ON CONFLICT (id) DO NOTHING;

INSERT INTO courses (id, title, description, instructor_id, category, level, price, cover_image, total_lessons, total_duration, status, rating, student_count) VALUES
  (1, 'Vue 3 企业项目实战', '从组合式 API 到权限、支付与部署的完整课程。', 2, '编程', 'INTERMEDIATE', 199.00, 'https://images.unsplash.com/photo-1516321318423-f06f85e504b3', 3, 95, 'PUBLISHED', 4.8, 1),
  (2, '产品设计入门', '面向零基础学员的设计思维与原型工作流。', 2, '设计', 'BEGINNER', 0.00, 'https://images.unsplash.com/photo-1518005020951-eccb494ad742', 2, 50, 'PUBLISHED', 4.6, 0)
ON CONFLICT (id) DO NOTHING;

INSERT INTO chapters (id, course_id, title, sort_order) VALUES
  (1, 1, '项目准备', 1),
  (2, 1, '核心功能实现', 2),
  (3, 2, '设计基础', 1)
ON CONFLICT (id) DO NOTHING;

INSERT INTO lessons (id, chapter_id, title, type, content, duration, is_free, sort_order) VALUES
  (1, 1, '课程导学', 'TEXT', '欢迎来到 EduFlow 课程，本节介绍学习路线。', 15, TRUE, 1),
  (2, 1, '环境搭建视频', 'VIDEO', 'https://example.com/videos/setup.mp4', 35, TRUE, 2),
  (3, 2, '权限测验', 'QUIZ', '{"questions":[{"title":"JWT 用于什么？","answer":"身份认证"}]}', 45, FALSE, 1),
  (4, 3, '设计思维概览', 'TEXT', '理解用户、定义问题、发散方案、验证原型。', 25, TRUE, 1)
ON CONFLICT (id) DO NOTHING;

INSERT INTO enrollments (id, user_id, course_id, progress) VALUES
  (1, 3, 1, 33.33)
ON CONFLICT (id) DO NOTHING;

INSERT INTO lesson_progress (id, enrollment_id, lesson_id, score) VALUES
  (1, 1, 1, NULL)
ON CONFLICT (id) DO NOTHING;

SELECT setval('users_id_seq', 10, true);
SELECT setval('courses_id_seq', 10, true);
SELECT setval('chapters_id_seq', 10, true);
SELECT setval('lessons_id_seq', 10, true);
SELECT setval('enrollments_id_seq', 10, true);
SELECT setval('lesson_progress_id_seq', 10, true);
