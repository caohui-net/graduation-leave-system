from rest_framework import serializers


class MobileLoginSerializer(serializers.Serializer):
    """移动端登录请求"""
    tenant_code = serializers.CharField(required=True)
    appid = serializers.CharField(required=True)
    saas_wap_token = serializers.CharField(required=True)


class AdminLoginSerializer(serializers.Serializer):
    """管理端登录请求"""
    authorization = serializers.CharField(required=True)


class UserSerializer(serializers.Serializer):
    """用户信息响应"""
    id = serializers.IntegerField()
    username = serializers.CharField()
    real_name = serializers.CharField()
    role = serializers.CharField()


class LoginResponseSerializer(serializers.Serializer):
    """登录响应"""
    token = serializers.CharField()
    user = UserSerializer()
