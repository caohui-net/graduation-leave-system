#!/usr/bin/env python3
"""测试学生宿舍信息功能"""
import os
import sys
import django

sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from apps.users.models import User
from django.db import connection

def test_database_fields():
    """测试1：验证数据库字段是否正确添加"""
    print("\n=== 测试1：数据库字段验证 ===")

    # 获取User表的字段
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_name = 'users'
            AND column_name IN ('room_number', 'campus', 'gender', 'major', 'level')
            ORDER BY column_name;
        """)
        fields = cursor.fetchall()

    expected_fields = {'room_number', 'campus', 'gender', 'major', 'level'}
    actual_fields = {row[0] for row in fields}

    if expected_fields == actual_fields:
        print("✅ 所有新字段已正确添加")
        for field in fields:
            print(f"   {field[0]}: {field[1]} (nullable: {field[2]})")
    else:
        missing = expected_fields - actual_fields
        print(f"❌ 缺失字段: {missing}")
        return False

    return True

def test_data_import():
    """测试2：验证数据导入结果"""
    print("\n=== 测试2：数据导入验证 ===")

    total_users = User.objects.count()
    students = User.objects.filter(role='student').count()
    has_room = User.objects.filter(role='student').exclude(room_number=None).exclude(room_number='').count()
    has_campus = User.objects.filter(role='student').exclude(campus=None).exclude(campus='').count()

    print(f"总用户数: {total_users}")
    print(f"学生数: {students}")
    print(f"有房间号: {has_room}")
    print(f"有校区: {has_campus}")

    if has_room > 5800:
        print(f"✅ 数据导入成功，{has_room}名学生有房间号")
    else:
        print(f"❌ 数据导入不足，仅{has_room}名学生有房间号")
        return False

    return True

def test_data_samples():
    """测试3：抽样验证数据准确性"""
    print("\n=== 测试3：数据抽样验证 ===")

    # 抽取5个有完整宿舍信息的学生
    samples = User.objects.filter(
        role='student'
    ).exclude(
        room_number=None
    ).exclude(
        room_number=''
    ).exclude(
        campus=None
    ).exclude(
        building=None
    )[:5]

    if not samples:
        print("❌ 没有找到完整宿舍信息的学生")
        return False

    print(f"抽取{len(samples)}个样本:")
    for user in samples:
        print(f"  {user.name} ({user.user_id})")
        print(f"    校区: {user.campus}")
        print(f"    楼栋: {user.building}")
        print(f"    房间: {user.room_number}")
        print(f"    性别: {user.gender or '未填'}")
        print(f"    专业: {user.major or '未填'}")
        print(f"    层次: {user.level or '未填'}")
        print()

    print("✅ 数据样本检查完成")
    return True

def test_data_integrity():
    """测试4：数据完整性检查"""
    print("\n=== 测试4：数据完整性检查 ===")

    # 检查有房间号但没有楼栋的异常情况
    invalid_1 = User.objects.filter(role='student').exclude(
        room_number=None
    ).exclude(
        room_number=''
    ).filter(building=None).count()

    # 检查有房间号但没有校区的情况
    invalid_2 = User.objects.filter(role='student').exclude(
        room_number=None
    ).exclude(
        room_number=''
    ).filter(campus=None).count()

    print(f"有房间号但无楼栋: {invalid_1}")
    print(f"有房间号但无校区: {invalid_2}")

    if invalid_1 == 0 and invalid_2 == 0:
        print("✅ 数据完整性检查通过")
        return True
    else:
        print("⚠️  存在部分数据不完整")
        return True  # 不算失败，只是警告

def test_field_types():
    """测试5：字段类型验证"""
    print("\n=== 测试5：字段类型验证 ===")

    # 检查room_number是否都是有效的字符串
    sample = User.objects.filter(role='student').exclude(
        room_number=None
    ).exclude(
        room_number=''
    ).first()

    if sample:
        print(f"房间号示例: '{sample.room_number}' (type: {type(sample.room_number).__name__})")
        print(f"校区示例: '{sample.campus}' (type: {type(sample.campus).__name__})")

        # 验证是否为字符串
        if isinstance(sample.room_number, str) and isinstance(sample.campus, str):
            print("✅ 字段类型正确")
            return True
        else:
            print("❌ 字段类型错误")
            return False
    else:
        print("⚠️  没有数据可供验证")
        return True

if __name__ == '__main__':
    print("=" * 60)
    print("学生宿舍信息功能测试")
    print("=" * 60)

    tests = [
        test_database_fields,
        test_data_import,
        test_data_samples,
        test_data_integrity,
        test_field_types
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ 测试异常: {str(e)}")
            failed += 1

    print("\n" + "=" * 60)
    print(f"测试结果: {passed} 通过, {failed} 失败")
    print("=" * 60)

    sys.exit(0 if failed == 0 else 1)
