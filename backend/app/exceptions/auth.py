class AuthException(Exception):
    def __init__(self, message: str = "认证失败"):
        self.message = message
        super().__init__(message)


class PermissionDeniedException(Exception):
    def __init__(self, message: str = "无权限访问"):
        self.message = message
        super().__init__(message)
