class PaymentFailedException(Exception):
    def __init__(self, message: str = "支付处理失败"):
        self.message = message
        super().__init__(message)


class InvalidOrderTransitionException(Exception):
    def __init__(self, message: str = "订单状态不允许执行该操作"):
        self.message = message
        super().__init__(message)
