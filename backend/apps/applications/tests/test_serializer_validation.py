from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from apps.applications.serializers import ApplicationCreateSerializer


class ApplicationCreateSerializerTest(TestCase):
    def test_reason_max_length_500(self):
        """Test reason field enforces 500 character limit"""
        data = {
            'reason': 'a' * 501,
            'leave_date': (timezone.now().date() + timedelta(days=1)).isoformat()
        }
        serializer = ApplicationCreateSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('reason', serializer.errors)

    def test_reason_empty_after_trim(self):
        """Test reason field rejects empty string after trim"""
        data = {
            'reason': '   ',
            'leave_date': (timezone.now().date() + timedelta(days=1)).isoformat()
        }
        serializer = ApplicationCreateSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('reason', serializer.errors)

    def test_leave_date_past(self):
        """Test leave_date field rejects dates before today"""
        data = {
            'reason': '毕业离校',
            'leave_date': (timezone.now().date() - timedelta(days=1)).isoformat()
        }
        serializer = ApplicationCreateSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('leave_date', serializer.errors)

    def test_leave_date_today(self):
        """Test leave_date field accepts today"""
        data = {
            'reason': '毕业离校',
            'leave_date': timezone.now().date().isoformat()
        }
        serializer = ApplicationCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_valid_data(self):
        """Test serializer accepts valid data"""
        data = {
            'reason': '毕业离校',
            'leave_date': (timezone.now().date() + timedelta(days=1)).isoformat()
        }
        serializer = ApplicationCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['reason'], '毕业离校')
