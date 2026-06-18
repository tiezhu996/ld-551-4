import logging

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.constants.enums import CourseStatus, OrderStatus, UserRole
from app.exceptions.auth import AuthException, PermissionDeniedException
from app.exceptions.course import CourseNotFoundException, CoursePermissionException
from app.exceptions.payment import InvalidOrderTransitionException, PaymentFailedException

logger = logging.getLogger(__name__)


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except HTTPException as exc:
            return JSONResponse(status_code=exc.status_code, content={"code": exc.status_code, "message": exc.detail, "detail": None})
        except (AuthException, PermissionDeniedException, CoursePermissionException) as exc:
            return JSONResponse(status_code=403, content={"code": 403, "message": exc.message, "detail": None})
        except CourseNotFoundException as exc:
            return JSONResponse(status_code=404, content={"code": 404, "message": exc.message, "detail": None})
        except (PaymentFailedException, InvalidOrderTransitionException) as exc:
            return JSONResponse(status_code=400, content={"code": 400, "message": exc.message, "detail": None})
        except Exception as exc:
            enum_hint = {
                "course_status": [item.value for item in CourseStatus],
                "order_status": [item.value for item in OrderStatus],
                "roles": [item.value for item in UserRole],
            }
            logger.exception("Unhandled error on %s %s", request.method, request.url.path)
            return JSONResponse(status_code=500, content={"code": 500, "message": "服务器错误，请稍后重试", "detail": {"error": str(exc), "enums": enum_hint}})
