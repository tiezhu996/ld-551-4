CREATE TYPE user_role AS ENUM ('STUDENT', 'INSTRUCTOR', 'ADMIN');
CREATE TYPE course_status AS ENUM ('DRAFT', 'PUBLISHED', 'ARCHIVED');
CREATE TYPE course_level AS ENUM ('BEGINNER', 'INTERMEDIATE', 'ADVANCED');
CREATE TYPE lesson_type AS ENUM ('VIDEO', 'TEXT', 'QUIZ');
CREATE TYPE order_status AS ENUM ('PENDING', 'PAID', 'REFUNDED', 'CANCELLED');

CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  name VARCHAR(120) NOT NULL,
  hashed_password VARCHAR(255) NOT NULL,
  role user_role NOT NULL DEFAULT 'STUDENT',
  bio VARCHAR(500)
);

CREATE TABLE IF NOT EXISTS courses (
  id SERIAL PRIMARY KEY,
  title VARCHAR(200) NOT NULL,
  description TEXT NOT NULL,
  instructor_id INTEGER NOT NULL REFERENCES users(id),
  category VARCHAR(80) NOT NULL,
  level course_level NOT NULL,
  price NUMERIC(10,2) NOT NULL DEFAULT 0,
  cover_image VARCHAR(500) NOT NULL,
  total_lessons INTEGER NOT NULL DEFAULT 0,
  total_duration INTEGER NOT NULL DEFAULT 0,
  status course_status NOT NULL DEFAULT 'DRAFT',
  rating DOUBLE PRECISION NOT NULL DEFAULT 0,
  student_count INTEGER NOT NULL DEFAULT 0,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS chapters (
  id SERIAL PRIMARY KEY,
  course_id INTEGER NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
  title VARCHAR(200) NOT NULL,
  sort_order INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS lessons (
  id SERIAL PRIMARY KEY,
  chapter_id INTEGER NOT NULL REFERENCES chapters(id) ON DELETE CASCADE,
  title VARCHAR(200) NOT NULL,
  type lesson_type NOT NULL,
  content TEXT NOT NULL,
  duration INTEGER NOT NULL DEFAULT 0,
  is_free BOOLEAN NOT NULL DEFAULT FALSE,
  sort_order INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS enrollments (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id),
  course_id INTEGER NOT NULL REFERENCES courses(id),
  enrolled_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  progress DOUBLE PRECISION NOT NULL DEFAULT 0,
  last_access_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  CONSTRAINT uq_enrollment_user_course UNIQUE (user_id, course_id)
);

CREATE TABLE IF NOT EXISTS lesson_progress (
  id SERIAL PRIMARY KEY,
  enrollment_id INTEGER NOT NULL REFERENCES enrollments(id) ON DELETE CASCADE,
  lesson_id INTEGER NOT NULL REFERENCES lessons(id),
  completed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  score INTEGER,
  CONSTRAINT uq_progress_enrollment_lesson UNIQUE (enrollment_id, lesson_id)
);

CREATE TABLE IF NOT EXISTS orders (
  id SERIAL PRIMARY KEY,
  order_no VARCHAR(64) UNIQUE NOT NULL,
  user_id INTEGER NOT NULL REFERENCES users(id),
  course_id INTEGER NOT NULL REFERENCES courses(id),
  amount NUMERIC(10,2) NOT NULL,
  payment_method VARCHAR(30) NOT NULL DEFAULT 'mock',
  status order_status NOT NULL DEFAULT 'PENDING',
  paid_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS audit_logs (
  id SERIAL PRIMARY KEY,
  user_id INTEGER,
  action VARCHAR(30) NOT NULL,
  entity VARCHAR(80) NOT NULL,
  entity_id VARCHAR(80),
  before_data JSONB,
  after_data JSONB,
  ip_address VARCHAR(80),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_courses_public_search ON courses(status, category, level, created_at);
CREATE INDEX IF NOT EXISTS idx_lessons_chapter ON lessons(chapter_id, sort_order);
CREATE INDEX IF NOT EXISTS idx_orders_user_status ON orders(user_id, status);
