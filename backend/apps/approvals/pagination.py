from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


class ApprovalLimitOffsetPagination(LimitOffsetPagination):
    """自定义分页器 - 只返回count和results"""
    default_limit = 20
    max_limit = 100000  # 支持大批量导出

    def get_paginated_response(self, data):
        return Response({
            'count': self.count,
            'results': data,
        })
