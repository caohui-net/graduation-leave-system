import os
import tempfile
from io import StringIO
from django.test import TestCase
from django.core.management import call_command
from django.core.management.base import CommandError
from apps.users.models import User, UserRole
from apps.users.class_mapping import ClassMapping


class ImportCSVCommandTest(TestCase):
    def setUp(self):
        """Create test counselors for mapping validation"""
        User.objects.create_user(user_id='T001', name='李老师', role=UserRole.COUNSELOR, password='T001')
        User.objects.create_user(user_id='T002', name='王老师', role=UserRole.COUNSELOR, password='T002')

    def create_temp_csv(self, content):
        """Helper to create temporary CSV file"""
        f = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv', encoding='utf-8')
        f.write(content)
        f.close()
        return f.name

    def test_import_counselors_success(self):
        """Test successful counselor import"""
        csv_content = "employee_id,name,department\nT003,张老师,计算机学院\nT004,赵老师,软件学院"
        filepath = self.create_temp_csv(csv_content)

        try:
            out = StringIO()
            call_command('import_csv', '--counselors', filepath, stdout=out)

            self.assertEqual(User.objects.filter(role=UserRole.COUNSELOR).count(), 4)
            self.assertTrue(User.objects.filter(user_id='T003', name='张老师').exists())
            self.assertIn('Created counselor: T003', out.getvalue())
        finally:
            os.unlink(filepath)

    def test_import_counselors_missing_required_field(self):
        """Test counselor import with missing required field"""
        csv_content = "employee_id\nT003"
        filepath = self.create_temp_csv(csv_content)

        try:
            with self.assertRaises(CommandError) as cm:
                call_command('import_csv', '--counselors', filepath)
            self.assertIn('missing required columns', str(cm.exception).lower())
        finally:
            os.unlink(filepath)

    def test_import_counselors_duplicate_in_csv(self):
        """Test counselor import with duplicate IDs in CSV"""
        csv_content = "employee_id,name\nT003,张老师\nT003,李老师"
        filepath = self.create_temp_csv(csv_content)

        try:
            out = StringIO()
            call_command('import_csv', '--counselors', filepath, stdout=out)
            output = out.getvalue()

            self.assertIn('Duplicate employee_id', output)
            self.assertIn('Failed:  1', output)
        finally:
            os.unlink(filepath)

    def test_import_mappings_success(self):
        """Test successful mapping import"""
        csv_content = "class_id,counselor_employee_id\nCS2020-01,T001\nCS2020-02,T002"
        filepath = self.create_temp_csv(csv_content)

        try:
            out = StringIO()
            call_command('import_csv', '--mappings', filepath, stdout=out)

            self.assertEqual(ClassMapping.objects.count(), 2)
            mapping = ClassMapping.objects.get(class_id='CS2020-01')
            self.assertEqual(mapping.counselor.user_id, 'T001')
        finally:
            os.unlink(filepath)

    def test_import_mappings_counselor_not_found(self):
        """Test mapping import with non-existent counselor"""
        csv_content = "class_id,counselor_employee_id\nCS2020-01,T999"
        filepath = self.create_temp_csv(csv_content)

        try:
            out = StringIO()
            call_command('import_csv', '--mappings', filepath, stdout=out)
            output = out.getvalue()

            self.assertIn('not found', output)
            self.assertIn('Failed:  1', output)
            self.assertEqual(ClassMapping.objects.count(), 0)
        finally:
            os.unlink(filepath)

    def test_import_students_success(self):
        """Test successful student import"""
        counselor = User.objects.get(user_id='T001')
        ClassMapping.objects.create(class_id='CS2020-01', counselor=counselor, counselor_name='李老师')

        csv_content = "student_id,name,class_id,is_graduating,graduation_year\n2020001,张三,CS2020-01,true,2024"
        filepath = self.create_temp_csv(csv_content)

        try:
            out = StringIO()
            call_command('import_csv', '--students', filepath, stdout=out)

            self.assertEqual(User.objects.filter(role=UserRole.STUDENT).count(), 1)
            student = User.objects.get(user_id='2020001')
            self.assertEqual(student.name, '张三')
            self.assertEqual(student.class_id, 'CS2020-01')
            self.assertTrue(student.is_graduating)
        finally:
            os.unlink(filepath)

    def test_import_students_class_mapping_missing(self):
        """Test student import with missing class mapping"""
        csv_content = "student_id,name,class_id,is_graduating,graduation_year\n2020001,张三,CS2020-99,true,2024"
        filepath = self.create_temp_csv(csv_content)

        try:
            out = StringIO()
            call_command('import_csv', '--students', filepath, stdout=out)
            output = out.getvalue()

            self.assertIn('no counselor mapping', output)
            self.assertIn('Failed:  1', output)
            self.assertEqual(User.objects.filter(role=UserRole.STUDENT).count(), 0)
        finally:
            os.unlink(filepath)

    def test_dry_run_mode(self):
        """Test dry-run mode doesn't apply changes"""
        csv_content = "employee_id,name\nT005,测试老师"
        filepath = self.create_temp_csv(csv_content)

        try:
            out = StringIO()
            call_command('import_csv', '--counselors', filepath, '--dry-run', stdout=out)
            output = out.getvalue()

            self.assertIn('DRY RUN', output)
            self.assertIn('Created: 1', output)
            self.assertFalse(User.objects.filter(user_id='T005').exists())
        finally:
            os.unlink(filepath)

    def test_validation_error_skips_invalid_rows(self):
        """Test that validation errors skip invalid rows but import valid ones"""
        csv_content = "employee_id,name\nT006,老师A\nT007,老师B\n,老师C"
        filepath = self.create_temp_csv(csv_content)

        try:
            initial_count = User.objects.filter(role=UserRole.COUNSELOR).count()
            out = StringIO()
            call_command('import_csv', '--counselors', filepath, stdout=out)
            output = out.getvalue()

            # Valid rows should be imported, invalid row should be skipped
            final_count = User.objects.filter(role=UserRole.COUNSELOR).count()
            self.assertEqual(final_count, initial_count + 2)
            self.assertIn('Created: 2', output)
            self.assertIn('Failed:  1', output)
            self.assertIn('Missing required field', output)
        finally:
            os.unlink(filepath)
