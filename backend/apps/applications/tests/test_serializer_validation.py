from django.test import TestCase
from django.utils import timezone
from datetime import timedelta, datetime
from unittest.mock import patch
from apps.applications.serializers import ApplicationCreateSerializer


class ApplicationCreateSerializerTest(TestCase):
    def test_reason_max_length_500(self):
        """Test reason field enforces 500 character limit"""
        data = {
            'contact_phone': '13800138000',
            'reason': 'a' * 501,
            'leave_date': (timezone.now().date() + timedelta(days=1)).isoformat()
        }
        serializer = ApplicationCreateSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('reason', serializer.errors)

    def test_reason_empty_after_trim(self):
        """Test reason field rejects empty string after trim"""
        data = {
            'contact_phone': '13800138000',
            'reason': '   ',
            'leave_date': (timezone.now().date() + timedelta(days=1)).isoformat()
        }
        serializer = ApplicationCreateSerializer(data=data)
        # Reason is now optional, so this should pass validation
        self.assertTrue(serializer.is_valid())

    def test_leave_date_past(self):
        """Test leave_date field rejects dates before today"""
        data = {
            'contact_phone': '13800138000',
            'reason': '毕业离校',
            'leave_date': (timezone.now().date() - timedelta(days=1)).isoformat()
        }
        serializer = ApplicationCreateSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('leave_date', serializer.errors)

    def test_leave_date_today(self):
        """Test leave_date field accepts today"""
        data = {
            'contact_phone': '13800138000',
            'reason': '毕业离校',
            'leave_date': timezone.now().date().isoformat()
        }
        serializer = ApplicationCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_valid_data(self):
        """Test serializer accepts valid data"""
        data = {
            'contact_phone': '13800138000',
            'reason': '毕业离校',
            'leave_date': (timezone.now().date() + timedelta(days=1)).isoformat()
        }
        serializer = ApplicationCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['reason'], '毕业离校')

    @patch('django.utils.timezone.now')
    def test_leave_date_validation_at_midnight_boundary(self, mock_now):
        """Test leave_date validation at 23:59:59 boundary"""
        # Mock timezone.now() to 2026-06-01 23:59:59 Asia/Shanghai
        mock_now.return_value = timezone.make_aware(
            datetime(2026, 6, 1, 23, 59, 59),
            timezone.get_current_timezone()
        )

        # Submit with leave_date=tomorrow (2026-06-02)
        data = {
            'contact_phone': '13800138000',
            'reason': '毕业离校',
            'leave_date': '2026-06-02'
        }
        serializer = ApplicationCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    @patch('django.utils.timezone.now')
    def test_leave_date_validation_after_midnight(self, mock_now):
        """Test leave_date validation rejects past date after midnight"""
        # Mock timezone.now() to 2026-06-02 00:00:01 Asia/Shanghai
        mock_now.return_value = timezone.make_aware(
            datetime(2026, 6, 2, 0, 0, 1),
            timezone.get_current_timezone()
        )

        # Submit with leave_date=yesterday (2026-06-01)
        data = {
            'contact_phone': '13800138000',
            'reason': '毕业离校',
            'leave_date': '2026-06-01'
        }
        serializer = ApplicationCreateSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('leave_date', serializer.errors)
