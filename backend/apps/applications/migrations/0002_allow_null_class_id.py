from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='class_id',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
    ]
