import logging
import traceback

logger = logging.getLogger(__name__)


class ErrorLoggingMiddleware:
    """记录所有未捕获的异常到日志"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        """捕获视图中未处理的异常"""
        user_id = getattr(request.user, 'user_id', 'anonymous')

        logger.error(
            f"Unhandled exception in {request.method} {request.path}",
            extra={
                'user_id': user_id,
                'method': request.method,
                'path': request.path,
                'query_params': dict(request.GET),
                'exception_type': type(exception).__name__,
                'exception_message': str(exception),
                'traceback': traceback.format_exc()
            },
            exc_info=True
        )

        # 返回None让Django使用默认错误处理
        return None
