from django.db import migrations
from django.utils import timezone


def add_test_user(apps, schema_editor):
    User = apps.get_model('users', 'User')
    db = schema_editor.connection.alias
    if not User.objects.using(db).filter(user_id='test_temp_001').exists():
        User.objects.using(db).create(
            user_id='test_temp_001',
            name='测试临时用户',
            role='student',
            department='计算机学院',
            phone='13800000001',
            email='',
            active=True,
            is_graduating=True,
            is_superuser=False,
            is_staff=False,
            is_demo=False,
            password='unusable',
            created_at=timezone.now(),
            updated_at=timezone.now(),
        )


def remove_test_user(apps, schema_editor):
    apps.get_model('users', 'User').objects.using(
        schema_editor.connection.alias
    ).filter(user_id='test_temp_001').delete()


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0009_merge_user_92005340_into_20240061'),
    ]

    operations = [
        migrations.RunPython(add_test_user, remove_test_user),
    ]
