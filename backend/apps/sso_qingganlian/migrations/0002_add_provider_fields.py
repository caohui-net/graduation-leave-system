# Generated manually for SSO generalization - Phase 1
# Adds provider, external_uid, provider_data fields with data backfill

from django.db import migrations, models


def backfill_provider_data(apps, schema_editor):
    """Backfill existing SSOUserMapping records with new provider fields"""
    SSOUserMapping = apps.get_model('sso_qingganlian', 'SSOUserMapping')

    for mapping in SSOUserMapping.objects.all():
        mapping.provider = 'qingganlian'
        mapping.external_uid = mapping.tenant_code
        mapping.provider_data = {
            'tenant_code': mapping.tenant_code,
            'user_code': mapping.user_code,
            'username': mapping.username,
        }
        mapping.save(update_fields=['provider', 'external_uid', 'provider_data'])


def reverse_backfill(apps, schema_editor):
    """Reverse migration - clear new fields"""
    SSOUserMapping = apps.get_model('sso_qingganlian', 'SSOUserMapping')
    SSOUserMapping.objects.all().update(
        provider=None,
        external_uid=None,
        provider_data=None
    )


class Migration(migrations.Migration):

    dependencies = [
        ('sso_qingganlian', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ssousermapping',
            name='provider',
            field=models.CharField(max_length=50, null=True, blank=True, verbose_name='SSO提供商'),
        ),
        migrations.AddField(
            model_name='ssousermapping',
            name='external_uid',
            field=models.CharField(max_length=200, null=True, blank=True, verbose_name='外部用户ID'),
        ),
        migrations.AddField(
            model_name='ssousermapping',
            name='provider_data',
            field=models.JSONField(null=True, blank=True, verbose_name='提供商数据'),
        ),
        migrations.RunPython(backfill_provider_data, reverse_backfill),
    ]
