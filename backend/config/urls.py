"""URL Configuration"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.users.urls')),
    path('api/', include('apps.attachments.urls')),
    path('api/applications/', include('apps.applications.urls')),
    path('api/approvals/', include('apps.approvals.urls')),
]
