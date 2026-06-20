from django.db import migrations


def merge_user(apps, schema_editor):
    """将旧工号 92005340 的审批记录迁移到新工号 20240061，并删除旧用户。"""
    db = schema_editor.connection.alias
    Approval = apps.get_model('approvals', 'Approval')
    User = apps.get_model('users', 'User')

    old_id = '92005340'
    new_id = '20240061'

    if not User.objects.using(db).filter(user_id=old_id).exists():
        return  # 已清理，幂等跳过

    Approval.objects.using(db).filter(approver_id=old_id).update(approver_id=new_id)
    User.objects.using(db).filter(user_id=old_id).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0008_add_room_and_student_info'),
    ]

    operations = [
        migrations.RunPython(merge_user, migrations.RunPython.noop),
    ]
