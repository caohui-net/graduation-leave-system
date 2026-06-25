from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseSSOProvider(ABC):
    """SSO提供商抽象基类

    保留理由: views.py 依赖此接口契约，提供多SSO扩展点（如未来对接CAS/统一身份认证）
    删除条件: 确认无第二实现计划 AND 视图层改为直接依赖具体类 AND 单元测试不使用mock替身
    决策来源: ponytail-audit-final-consensus.md (2026-06-24)
    """

    @abstractmethod
    def authenticate(self, credentials: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行SSO认证流程

        Args:
            credentials: 认证凭证（前端传入的参数）

        Returns:
            标准化的用户信息字典：
            {
                'external_uid': str,      # 外部用户唯一标识
                'external_username': str, # 外部用户名（可选）
                'real_name': str,         # 真实姓名
                'phone': str,             # 手机号（可选）
                'email': str,             # 邮箱（可选）
                'provider_data': dict     # 提供商特定数据
            }

        Raises:
            SSOAPIError: 认证失败
        """
        pass

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """提供商名称（如 'qingganlian', 'dingtalk'）"""
        pass
