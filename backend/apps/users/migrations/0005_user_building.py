from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_backfill_dorm_manager'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='building',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
