"""URL Configuration"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.http import HttpResponseRedirect
from django.conf import settings
from django.views.static import serve
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from apps.healthcheck.views import healthz, readyz, version
import os

DEMO_WEB_V2 = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'demo-web-v2')

urlpatterns = [
    path('', lambda request: HttpResponseRedirect(settings.FRONTEND_URL)),
    path('healthz', healthz, name='healthz'),
    path('readyz', readyz, name='readyz'),
    path('version', version, name='version'),
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.users.urls')),
    path('api/', include('apps.attachments.urls')),
    path('api/applications/', include('apps.applications.urls')),
    path('api/approvals/', include('apps.approvals.urls')),
    path('api/notifications/', include('apps.notifications.urls')),
    path('api/sso/qingganlian/', include('apps.sso_qingganlian.urls')),

    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # demo-web-v2 本地预览（开发用）
    path('v2/', lambda r: serve(r, 'index.html', document_root=DEMO_WEB_V2)),
    re_path(r'^v2/(?P<path>.+)$', serve, {'document_root': DEMO_WEB_V2}),
]
