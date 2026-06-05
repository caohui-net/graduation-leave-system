#!/usr/bin/env python3
"""
Temporary user ID generation for students without student numbers.
Handles graduate students and File2 unmatched students.
"""
import hashlib
from typing import Tuple


def generate_grad_user_id(name: str, college: str, building: str, room: str) -> str:
    """
    Generate stable ID for graduate students without XH.
    Format: GRAD2026_{hash8}
    """
    # Create stable hash from multiple fields
    data = f"{name}|{college}|{building}|{room}".encode('utf-8')
    hash_hex = hashlib.sha256(data).hexdigest()[:8]
    return f"GRAD2026_{hash_hex.upper()}"


def generate_tmp_user_id(row_index: int) -> str:
    """
    Generate temporary ID for File2 unmatched students.
    Format: TMP2026_{row_number:04d}
    """
    return f"TMP2026_{row_index:04d}"


def determine_user_id(
    student_no: str | None,
    name: str,
    college: str,
    building: str,
    room: str,
    row_index: int,
    is_graduate: bool = False
) -> Tuple[str, str]:
    """
    Determine final user_id and source for a student.

    Args:
        student_no: XH from File2 (may be None)
        name: Student name
        college: Normalized college name
        building: Building name
        room: Room number
        row_index: Row number in File1 (1-based)
        is_graduate: Whether student is graduate level

    Returns:
        (user_id, user_id_source) tuple
        user_id_source: 'file2_xh' | 'grad_generated' | 'tmp_generated'
    """
    # Priority 1: Real student number from File2
    if student_no and student_no.strip():
        return student_no.strip(), 'file2_xh'

    # Priority 2: Graduate student without XH
    if is_graduate:
        grad_id = generate_grad_user_id(name, college, building, room)
        return grad_id, 'grad_generated'

    # Priority 3: File2 unmatched undergraduate
    tmp_id = generate_tmp_user_id(row_index)
    return tmp_id, 'tmp_generated'


if __name__ == "__main__":
    # Test cases
    print("Test 1: Real student number")
    uid, source = determine_user_id("2020001", "张三", "计算机学院", "荷园1栋", "101", 1)
    print(f"  {uid} ({source})")
    assert uid == "2020001"
    assert source == "file2_xh"

    print("\nTest 2: Graduate student without XH")
    uid, source = determine_user_id(None, "李四", "数学学院", "荷园2栋", "201", 100, is_graduate=True)
    print(f"  {uid} ({source})")
    assert uid.startswith("GRAD2026_")
    assert source == "grad_generated"
    assert len(uid) == 17  # GRAD2026_ + 8 hex chars

    # Verify hash stability
    uid2, _ = determine_user_id(None, "李四", "数学学院", "荷园2栋", "201", 100, is_graduate=True)
    assert uid == uid2, "Hash must be stable"

    print("\nTest 3: File2 unmatched undergraduate")
    uid, source = determine_user_id(None, "王五", "物理学院", "荷园3栋", "301", 500)
    print(f"  {uid} ({source})")
    assert uid == "TMP2026_0500"
    assert source == "tmp_generated"

    print("\n✓ All tests passed")
