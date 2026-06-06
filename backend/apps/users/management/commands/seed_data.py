from django.core.management.base import BaseCommand
from apps.users.models import User, UserRole


class Command(BaseCommand):
    help = 'Load seed data for users'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Clear applications and approvals before loading seed data',
        )

    def handle(self, *args, **options):
        if options['reset']:
            self.stdout.write('Resetting applications and approvals...')
            from apps.applications.models import Application
            from apps.approvals.models import Approval
            Approval.objects.all().delete()
            Application.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Reset complete'))

        self.stdout.write('Loading seed data...')

        # Students (10)
        students = [
            {'user_id': '2020001', 'name': '张三', 'class_id': 'CS2020-01', 'building': '1号楼', 'department': '计算机学院'},
            {'user_id': '2020002', 'name': '李四', 'class_id': 'CS2020-02', 'building': '2号楼', 'department': '软件学院'},
            {'user_id': '2020003', 'name': '王五', 'class_id': 'CS2020-01', 'building': '1号楼', 'department': '计算机学院'},
            {'user_id': '2020004', 'name': '赵六', 'class_id': 'CS2020-01', 'building': '1号楼', 'department': '计算机学院'},
            {'user_id': '2020005', 'name': '孙七', 'class_id': 'CS2020-01', 'building': '1号楼', 'department': '计算机学院'},
            {'user_id': '2020006', 'name': '周八', 'class_id': 'CS2020-02', 'building': '2号楼', 'department': '软件学院'},
            {'user_id': '2020007', 'name': '吴九', 'class_id': 'CS2020-02', 'building': '2号楼', 'department': '软件学院'},
            {'user_id': '2020008', 'name': '郑十', 'class_id': 'CS2020-02', 'building': '2号楼', 'department': '软件学院'},
            {'user_id': '2020009', 'name': '王十一', 'class_id': 'CS2020-02', 'building': '2号楼', 'department': '软件学院'},
            {'user_id': '2020010', 'name': '王十二', 'class_id': 'CS2020-02', 'building': '2号楼', 'department': '软件学院'},
        ]

        for student_data in students:
            user, created = User.objects.update_or_create(
                user_id=student_data['user_id'],
                defaults={
                    'name': student_data['name'],
                    'role': UserRole.STUDENT,
                    'class_id': student_data['class_id'],
                    'building': student_data.get('building'),
                    'department': student_data.get('department'),
                    'is_graduating': True,
                    'graduation_year': 2024,
                    'active': True,
                }
            )
            if created:
                user.set_password(student_data['user_id'])
                user.save()
            self.stdout.write(f'{"Created" if created else "Updated"} student: {user.user_id}')

        # Counselors (2)
        counselors = [
            {'user_id': 'T001', 'name': '李老师', 'department': '计算机学院'},
            {'user_id': 'T002', 'name': '王老师', 'department': '软件学院'},
        ]

        for counselor_data in counselors:
            user, created = User.objects.get_or_create(
                user_id=counselor_data['user_id'],
                defaults={
                    'name': counselor_data['name'],
                    'role': UserRole.COUNSELOR,
                    'department': counselor_data.get('department'),
                    'active': True,
                }
            )
            if created:
                user.set_password(counselor_data['user_id'])
                user.save()
                self.stdout.write(f'Created counselor: {user.user_id}')

        # Dorm managers (2)
        dorm_managers = [
            {'user_id': 'M001', 'name': '宿管员1', 'building': '1号楼'},
            {'user_id': 'M002', 'name': '宿管员2', 'building': '2号楼'},
        ]

        for dm_data in dorm_managers:
            user, created = User.objects.update_or_create(
                user_id=dm_data['user_id'],
                defaults={
                    'name': dm_data['name'],
                    'role': UserRole.DORM_MANAGER,
                    'building': dm_data.get('building'),
                    'active': True,
                }
            )
            if created:
                user.set_password(dm_data['user_id'])
                user.save()
                self.stdout.write(f'Created dorm_manager: {user.user_id}')

        # Dean (1)
        user, created = User.objects.get_or_create(
            user_id='D001',
            defaults={
                'name': '赵主任',
                'role': UserRole.DEAN,
                'active': True,
            }
        )
        if created:
            user.set_password('D001')
            user.save()
            self.stdout.write(f'Created dean: {user.user_id}')

        self.stdout.write(self.style.SUCCESS('Seed data loaded successfully'))
