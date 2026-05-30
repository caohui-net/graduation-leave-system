from dataclasses import dataclass
from typing import Optional
from .models import DormCheckoutStatus


@dataclass
class DormCheckoutStatusDTO:
    student_id: str
    status: str
    checked_at: Optional[str]
    blocking_reason: Optional[str]
    provider_error_code: Optional[str]


class MockDormCheckoutProvider:
    def check_status(self, student_id: str) -> DormCheckoutStatusDTO:
        mock_data = {
            "2020001": DormCheckoutStatusDTO(
                student_id="2020001",
                status=DormCheckoutStatus.COMPLETED,
                checked_at="2024-05-15T10:00:00Z",
                blocking_reason=None,
                provider_error_code=None
            ),
            "2020002": DormCheckoutStatusDTO(
                student_id="2020002",
                status=DormCheckoutStatus.PENDING,
                checked_at=None,
                blocking_reason="宿舍物品未清理",
                provider_error_code=None
            ),
            "2020003": DormCheckoutStatusDTO(
                student_id="2020003",
                status=DormCheckoutStatus.NOT_STARTED,
                checked_at=None,
                blocking_reason="未提交清退申请",
                provider_error_code=None
            ),
            "2020099": DormCheckoutStatusDTO(
                student_id="2020099",
                status=DormCheckoutStatus.UNKNOWN,
                checked_at=None,
                blocking_reason="学生信息不存在",
                provider_error_code="STUDENT_NOT_FOUND"
            ),
        }

        return mock_data.get(student_id, DormCheckoutStatusDTO(
            student_id=student_id,
            status=DormCheckoutStatus.NOT_STARTED,
            checked_at=None,
            blocking_reason="未在宿舍系统中找到记录",
            provider_error_code=None
        ))
