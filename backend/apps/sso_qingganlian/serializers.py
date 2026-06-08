from rest_framework import serializers


class MobileLoginRequestSerializer(serializers.Serializer):
    """移动端登录请求序列化器"""
    tenant_code = serializers.CharField(max_length=50, required=True, help_text='租户Code')
    appid = serializers.CharField(max_length=50, required=True, help_text='产品标识')
    saas_wap_token = serializers.CharField(max_length=500, required=True, help_text='用户登录token')


class UserInfoSerializer(serializers.Serializer):
    """用户信息序列化器"""
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(read_only=True)
    real_name = serializers.CharField(read_only=True)
    role = serializers.CharField(read_only=True)
    phone = serializers.CharField(read_only=True, required=False)


class MobileLoginResponseSerializer(serializers.Serializer):
    """移动端登录响应序列化器"""
    token = serializers.CharField(read_only=True, help_text='本地JWT token')
    user = UserInfoSerializer(read_only=True)


class AdminLoginRequestSerializer(serializers.Serializer):
    """管理端登录请求序列化器"""
    authorization = serializers.CharField(max_length=1000, required=True, help_text='Authorization token')


class AdminLoginResponseSerializer(serializers.Serializer):
    """管理端登录响应序列化器"""
    token = serializers.CharField(read_only=True, help_text='本地JWT token')
    user = UserInfoSerializer(read_only=True)
