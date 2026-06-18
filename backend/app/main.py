from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import auth, courses, enrollments, instructor, lessons, orders
from app.core.config import settings
from app.core.database import Base, engine
from app.middleware.audit_log import AuditLogMiddleware
from app.middleware.error_handler import ErrorHandlerMiddleware
from app import models  # noqa: F401

app = FastAPI(title=settings.app_name)

app.add_middleware(ErrorHandlerMiddleware)
app.add_middleware(AuditLogMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def health():
    return {"status": "ok", "service": "eduflow-backend"}


app.include_router(auth.router, prefix="/api")
app.include_router(courses.router, prefix="/api")
app.include_router(lessons.router, prefix="/api")
app.include_router(enrollments.router, prefix="/api")
app.include_router(orders.router, prefix="/api")
app.include_router(instructor.router, prefix="/api")
