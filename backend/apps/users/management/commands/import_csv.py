import csv
from django.core.management.base import BaseCommand
from apps.users.models import User, UserRole
from apps.users.class_mapping import ClassMapping


class Command(BaseCommand):
    help = 'Import users and class mappings from CSV files'

    def add_arguments(self, parser):
        parser.add_argument('--students', type=str, help='Path to students CSV file')
        parser.add_argument('--counselors', type=str, help='Path to counselors CSV file')
        parser.add_argument('--mappings', type=str, help='Path to class mappings CSV file')

    def handle(self, *args, **options):
        if options['students']:
            self.import_students(options['students'])

        if options['counselors']:
            self.import_counselors(options['counselors'])

        if options['mappings']:
            self.import_mappings(options['mappings'])

    def import_students(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                user, created = User.objects.update_or_create(
                    user_id=row['student_id'],
                    defaults={
                        'name': row['name'],
                        'role': UserRole.STUDENT,
                        'class_id': row['class_id'],
                        'is_graduating': row.get('is_graduating', 'true').lower() == 'true',
                        'graduation_year': int(row.get('graduation_year', 2024)),
                        'active': row.get('active', 'true').lower() == 'true'
                    }
                )
                if created:
                    user.set_password(row.get('password', row['student_id']))
                    user.save()
                self.stdout.write(f'{"Created" if created else "Updated"} student: {user.user_id}')

    def import_counselors(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                user, created = User.objects.update_or_create(
                    user_id=row['employee_id'],
                    defaults={
                        'name': row['name'],
                        'role': UserRole.COUNSELOR,
                        'active': row.get('active', 'true').lower() == 'true'
                    }
                )
                if created:
                    user.set_password(row.get('password', row['employee_id']))
                    user.save()
                self.stdout.write(f'{"Created" if created else "Updated"} counselor: {user.user_id}')

    def import_mappings(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                counselor = User.objects.get(user_id=row['counselor_id'])
                mapping, created = ClassMapping.objects.update_or_create(
                    class_id=row['class_id'],
                    defaults={
                        'counselor': counselor,
                        'counselor_name': counselor.name,
                        'active': row.get('active', 'true').lower() == 'true'
                    }
                )
                self.stdout.write(f'{"Created" if created else "Updated"} mapping: {mapping.class_id} -> {counselor.user_id}')
