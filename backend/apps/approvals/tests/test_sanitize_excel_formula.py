import pytest
from apps.approvals.views import sanitize_excel_formula


@pytest.mark.parametrize("value,expected", [
    # Dangerous prefixes must be escaped
    ("=SUM(A1:A10)", "'=SUM(A1:A10)"),
    ("+1234", "'+1234"),
    ("-1234", "'-1234"),
    ("@user", "'@user"),
    # Normal values pass through unchanged
    ("张三", "张三"),
    ("2020001", "2020001"),
    ("普通文本", "普通文本"),
    # Edge cases
    (None, None),
    ("", ""),
    (123, "123"),
])
def test_sanitize_excel_formula(value, expected):
    assert sanitize_excel_formula(value) == expected
