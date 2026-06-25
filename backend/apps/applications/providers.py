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


_MOCK_DATA: dict = {
    "2020001": {"status": DormCheckoutStatus.COMPLETED, "checked_at": "2024-05-15T10:00:00Z", "blocking_reason": None, "provider_error_code": None},
    "2020002": {"status": DormCheckoutStatus.COMPLETED, "checked_at": "2024-05-15T10:15:00Z", "blocking_reason": None, "provider_error_code": None},
    "2020003": {"status": DormCheckoutStatus.NOT_STARTED, "checked_at": None, "blocking_reason": "未提交清退申请", "provider_error_code": None},
    "2020006": {"status": DormCheckoutStatus.COMPLETED, "checked_at": "2024-05-15T10:30:00Z", "blocking_reason": None, "provider_error_code": None},
    "2020099": {"status": DormCheckoutStatus.UNKNOWN, "checked_at": None, "blocking_reason": "学生信息不存在", "provider_error_code": "STUDENT_NOT_FOUND"},
    "2022240340415": {"status": DormCheckoutStatus.COMPLETED, "checked_at": "2024-05-15T10:00:00Z", "blocking_reason": None, "provider_error_code": None},
    "2022190140302": {"status": DormCheckoutStatus.COMPLETED, "checked_at": "2024-05-15T10:00:00Z", "blocking_reason": None, "provider_error_code": None},
    "2022190140325": {"status": DormCheckoutStatus.COMPLETED, "checked_at": "2024-05-15T10:00:00Z", "blocking_reason": None, "provider_error_code": None},
    "2022250140422": {"status": DormCheckoutStatus.COMPLETED, "checked_at": "2024-05-15T10:00:00Z", "blocking_reason": None, "provider_error_code": None},
    "2022220040109": {"status": DormCheckoutStatus.COMPLETED, "checked_at": "2024-05-15T10:00:00Z", "blocking_reason": None, "provider_error_code": None},
    "2022220040203": {"status": DormCheckoutStatus.COMPLETED, "checked_at": "2024-05-15T10:00:00Z", "blocking_reason": None, "provider_error_code": None},
    "2022250140610": {"status": DormCheckoutStatus.COMPLETED, "checked_at": "2024-05-15T10:00:00Z", "blocking_reason": None, "provider_error_code": None},
}

_DEFAULT_STATUS = {"status": DormCheckoutStatus.COMPLETED, "checked_at": "2024-06-01T00:00:00Z", "blocking_reason": None, "provider_error_code": None}


def get_dorm_checkout_status(student_id: str) -> DormCheckoutStatusDTO:
    data = _MOCK_DATA.get(student_id, _DEFAULT_STATUS)
    return DormCheckoutStatusDTO(student_id=student_id, **data)


# Backward-compatible alias for existing callers
class MockDormCheckoutProvider:
    def check_status(self, student_id: str) -> DormCheckoutStatusDTO:
        return get_dorm_checkout_status(student_id)
