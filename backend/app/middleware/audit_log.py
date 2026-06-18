import time

from starlette.middleware.base import BaseHTTPMiddleware


class AuditLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        request.state.started_at = time.time()
        response = await call_next(request)
        if request.method in {"POST", "PUT", "PATCH", "DELETE"}:
            duration_ms = round((time.time() - request.state.started_at) * 1000, 2)
            response.headers["X-Audit-Observed"] = f"{request.method}:{request.url.path}:{duration_ms}ms"
        return response
