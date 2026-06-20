from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0011_sync_test_record'),
    ]
    operations = [
        migrations.RunPython(
            lambda apps, se: apps.get_model('users', 'User').objects.using(se.connection.alias).filter(user_id='sync_test_001').delete(),
            migrations.RunPython.noop,
        ),
    ]
