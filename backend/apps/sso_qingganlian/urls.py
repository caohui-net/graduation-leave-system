from django.urls import path
from . import views
from . import callback_views

app_name = 'sso_qingganlian'

urlpatterns = [
    path('callback', callback_views.sso_callback, name='sso_callback'),  # HTML callback入口
    path('mobile/login', views.mobile_login, name='mobile_login'),
    path('mobile/saas-login', views.mobile_saas_login, name='mobile_saas_login'),
    path('admin/login', views.admin_login, name='admin_login'),
]
