from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'name', 'role', 'class_id', 'active', 'is_graduating', 'graduation_year']
        read_only_fields = ['user_id']


class AuthUserSerializer(serializers.ModelSerializer):
    """登录响应中的用户摘要（UserDTO子集）"""
    class Meta:
        model = User
        fields = ['user_id', 'name', 'role', 'class_id', 'phone', 'building', 'room_number']


class LoginSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user_id = attrs.get('user_id')
        password = attrs.get('password')

        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            raise serializers.ValidationError('Invalid credentials')

        if not user.check_password(password):
            raise serializers.ValidationError('Invalid credentials')

        if not user.active:
            raise serializers.ValidationError('Account is inactive')

        refresh = RefreshToken.for_user(user)

        return {
            'access_token': str(refresh.access_token),
            'token_type': 'Bearer',
            'user': AuthUserSerializer(user).data
        }


class LoginResponseSerializer(serializers.Serializer):
    """登录成功响应（schema-only，用于OpenAPI文档）"""
    access_token = serializers.CharField(help_text="JWT access token")
    token_type = serializers.CharField(default='Bearer', help_text="Token type")
    user = AuthUserSerializer(help_text="用户信息")


class DemoLoginSerializer(serializers.Serializer):
    """演示登录（仅在DEMO_AUTH_ENABLED=true时启用）"""
    role = serializers.ChoiceField(choices=['student', 'dorm_manager', 'counselor', 'dean'])

    # 角色到演示用户映射
    DEMO_USERS = {
        'student': '2020001',
        'dorm_manager': 'M001',
        'counselor': 'T001',
        'dean': 'D001',
    }

    def validate(self, attrs):
        role = attrs.get('role')
        user_id = self.DEMO_USERS.get(role)

        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            raise serializers.ValidationError(f'Demo user for role {role} not found')

        if not user.is_demo:
            raise serializers.ValidationError('This account is not marked as a demo account')

        if not user.active:
            raise serializers.ValidationError('Demo account is inactive')

        refresh = RefreshToken.for_user(user)

        return {
            'access_token': str(refresh.access_token),
            'token_type': 'Bearer',
            'user': AuthUserSerializer(user).data
        }
