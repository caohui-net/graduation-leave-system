"""
Schema-only serializers for OpenAPI documentation.
These serializers are used only for @extend_schema decorators and do not handle actual data serialization.
"""
from rest_framework import serializers


class ErrorDetailSerializer(serializers.Serializer):
    """Error detail structure used in project error envelope"""
    code = serializers.CharField(help_text="Error code (e.g., NOT_FOUND, FORBIDDEN)")
    message = serializers.CharField(help_text="Human-readable error message")
    details = serializers.JSONField(required=False, help_text="Additional error details")


class ErrorResponseSerializer(serializers.Serializer):
    """Project error envelope: {error: {code, message, details}}"""
    error = ErrorDetailSerializer()
