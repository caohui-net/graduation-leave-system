#!/usr/bin/env python3
"""
College name normalization for graduation leave system.
Maps File1 college names to File4 counselor department names.
"""

# College mapping from File1 (student data) to File4 (counselor data)
COLLEGE_NORMALIZATION_MAP = {
    # File1 format -> File4 format
    "文学院（苏东坡书院）": "文学院(苏东坡书院)",
    "文学院(苏东坡书院)": "文学院(苏东坡书院)",

    "政法学院、纪检监察学院、知识产权学院": "政法学院",
    "政法学院": "政法学院",

    "外国语学院": "外国语学院",

    "新闻与传播学院": "新闻与传播学院",

    "商学院": "商学院",

    "旅游文化与地理科学学院": "旅游文化与地理科学学院",

    "教育学院": "教育学院",

    "体育学院": "体育学院",

    "音乐与戏剧学院": "音乐与戏剧学院",

    "美术学院": "美术学院",

    "数学与统计学院": "数学与统计学院",

    "物理与电信学院": "物理与电信学院",

    "化学化工学院": "化学化工学院",

    "生命科学学院": "生命科学学院",

    "计算机学院": "计算机与人工智能学院",
    "计算机与人工智能学院": "计算机与人工智能学院",

    "建筑与工程学院": "建筑与工程学院",

    "电子信息学院": "电子信息学院",

    "马克思主义学院": "马克思主义学院",

    # Additional mappings discovered from File1 data (2026-06-05)
    "传媒与影视学院": "新闻与传播学院",
    "地理与旅游学院": "旅游文化与地理科学学院",
    "建筑工程学院": "建筑与工程学院",
    "机电与智能制造学院": "机电与智能制造学院",
    "李时珍中医药学院": "李时珍中医药学院",
    "生物与农业资源学院": "生命科学学院",
    "音乐学院、黄梅戏学院": "音乐与戏剧学院",
}


def normalize_college_name(college_name: str) -> str:
    """
    Normalize college name from File1 format to File4 format.

    Args:
        college_name: Raw college name from File1

    Returns:
        Normalized college name matching File4 format

    Raises:
        ValueError: If college name not in mapping
    """
    if not college_name or not college_name.strip():
        raise ValueError("College name cannot be empty")

    normalized = COLLEGE_NORMALIZATION_MAP.get(college_name.strip())
    if normalized is None:
        raise ValueError(f"Unknown college name: {college_name}")

    return normalized


def validate_mapping() -> bool:
    """Validate that all mappings are consistent."""
    # Check for duplicate values (multiple sources mapping to same target is OK)
    # Check for self-consistency (normalized value should map to itself)
    for source, target in COLLEGE_NORMALIZATION_MAP.items():
        if target in COLLEGE_NORMALIZATION_MAP:
            if COLLEGE_NORMALIZATION_MAP[target] != target:
                print(f"WARNING: Inconsistent mapping: {target} -> {COLLEGE_NORMALIZATION_MAP[target]}")
                return False
    return True


if __name__ == "__main__":
    # Validate mapping
    if validate_mapping():
        print("✓ College normalization mapping validated")
        print(f"✓ {len(set(COLLEGE_NORMALIZATION_MAP.values()))} unique colleges")
    else:
        print("✗ Mapping validation failed")
        exit(1)
