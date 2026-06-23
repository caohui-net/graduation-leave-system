from django.db import models
from django.core.exceptions import ValidationError
from apps.users.models import User


class ApplicationStatus(models.TextChoices):
    DRAFT = 'draft', '草稿'
    PENDING_DORM_MANAGER = 'pending_dorm_manager', '待宿管员审批'
    PENDING_COUNSELOR = 'pending_counselor', '待辅导员审批'
    APPROVED = 'approved', '已通过'
    REJECTED = 'rejected', '已驳回'
    FAILED = 'failed', '提交失败'


class DormCheckoutStatus(models.TextChoices):
    COMPLETED = 'completed', '已清退'
    PENDING = 'pending', '清退中'
    NOT_STARTED = 'not_started', '未开始'
    UNKNOWN = 'unknown', '状态未知'


class ApplicationType(models.TextChoices):
    LEAVE_SCHOOL = 'leave_school', '离校申请'
    STAY_SCHOOL = 'stay_school', '留校申请'
    LEAVE_REQUEST = 'leave_request', '请假申请'


class StayReason(models.TextChoices):
    EXAM_PREP = 'exam_prep', '考公考研'
    SUMMER_PRACTICE = 'summer_practice', '暑期实践'
    TEACHER_EXAM = 'teacher_exam', '考教师编'
    HUANGZHOU_INTERN = 'huangzhou_intern', '黄州实习'
    SPORTS_VOLUNTEER = 'sports_volunteer', '体育比赛志愿服务'
    CHALLENGE_CUP = 'challenge_cup', '挑战杯竞赛'
    COLLEGE_COMPETITION = 'college_competition', '学院组织的比赛'
    MENTOR_GUIDANCE = 'mentor_guidance', '导师指导'
    OTHER = 'other', '其它'


class Application(models.Model):
    application_id = models.CharField(max_length=50, primary_key=True)
    student = models.ForeignKey(User, on_delete=models.PROTECT, related_name='applications')
    student_name = models.CharField(max_length=100)
    class_id = models.CharField(max_length=50)
    contact_phone = models.CharField(max_length=20, null=True, blank=True)

    # 申请类型
    application_type = models.CharField(
        max_length=20,
        choices=ApplicationType.choices,
        default=ApplicationType.LEAVE_SCHOOL,
        verbose_name='申请类型'
    )

    # 留校申请字段
    stay_start_date = models.DateField(null=True, blank=True, verbose_name='留校开始日期')
    stay_end_date = models.DateField(null=True, blank=True, verbose_name='留校结束日期')
    stay_reason = models.CharField(
        max_length=30,
        choices=StayReason.choices,
        null=True,
        blank=True,
        verbose_name='留校原因'
    )

    reason = models.TextField(blank=True, default='')
    leave_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=ApplicationStatus.choices, default=ApplicationStatus.DRAFT)
    dorm_checkout_status = models.CharField(max_length=20, choices=DormCheckoutStatus.choices, default=DormCheckoutStatus.NOT_STARTED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'applications'

    def clean(self):
        active_statuses = [
            ApplicationStatus.PENDING_DORM_MANAGER,
            ApplicationStatus.PENDING_COUNSELOR,
            ApplicationStatus.APPROVED,
        ]
        if self.status in active_statuses:
            existing = Application.objects.filter(
                student=self.student,
                status__in=active_statuses
            ).exclude(application_id=self.application_id).exists()
            if existing:
                raise ValidationError('该学生已有待审批或已通过的申请，不能重复提交')
