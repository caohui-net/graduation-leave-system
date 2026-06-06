# Generated migration to add ADMIN role to User.role choices

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_user_building'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(
                choices=[
                    ('student', '学生'),
                    ('dorm_manager', '宿管员'),
                    ('counselor', '辅导员'),
                    ('dean', '学工部'),
                    ('admin', '学工管理员')
                ],
                max_length=20
            ),
        ),
    ]
