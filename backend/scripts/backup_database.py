#!/usr/bin/env python3
"""数据库备份脚本 - 绕过shell限制"""
import os
import sys
import django
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()

from django.core.management import call_command

timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
output_file = f'/tmp/pre_import_{timestamp}.json'

print(f"备份数据库到: {output_file}")
with open(output_file, 'w') as f:
    call_command('dumpdata', natural_foreign=True, natural_primary=True, stdout=f)

print(f"✓ 备份完成: {output_file}")
os.system(f'ls -lh {output_file}')
