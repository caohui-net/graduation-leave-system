from django.db import migrations
from django.utils import timezone


def add(apps, schema_editor):
    User = apps.get_model('users', 'User')
    db = schema_editor.connection.alias
    if not User.objects.using(db).filter(user_id='sync_test_002').exists():
        User.objects.using(db).create(
            user_id='sync_test_002', name='无重启同步测试', role='student',
            department='测试', phone='', email='', active=True,
            is_graduating=False, is_superuser=False, is_staff=False,
            is_demo=False, password='unusable',
            created_at=timezone.now(), updated_at=timezone.now(),
        )


def remove(apps, schema_editor):
    apps.get_model('users', 'User').objects.using(
        schema_editor.connection.alias
    ).filter(user_id='sync_test_002').delete()


class Migration(migrations.Migration):
    dependencies = [('users', '0012_remove_sync_test_record')]
    operations = [migrations.RunPython(add, remove)]
