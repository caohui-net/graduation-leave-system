from django.db import migrations
from django.utils import timezone


def add_sync_test(apps, schema_editor):
    User = apps.get_model('users', 'User')
    db = schema_editor.connection.alias
    if not User.objects.using(db).filter(user_id='sync_test_001').exists():
        User.objects.using(db).create(
            user_id='sync_test_001',
            name='同步测试用户',
            role='student',
            department='测试学院',
            phone='13900000001',
            email='',
            active=True,
            is_graduating=False,
            is_superuser=False,
            is_staff=False,
            is_demo=False,
            password='unusable',
            created_at=timezone.now(),
            updated_at=timezone.now(),
        )


def remove_sync_test(apps, schema_editor):
    apps.get_model('users', 'User').objects.using(
        schema_editor.connection.alias
    ).filter(user_id='sync_test_001').delete()


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0010_add_test_temp_user'),
    ]
    operations = [
        migrations.RunPython(add_sync_test, remove_sync_test),
    ]
