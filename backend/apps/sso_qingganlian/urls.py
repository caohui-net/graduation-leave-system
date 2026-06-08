from django.urls import path
from . import views

app_name = 'sso_qingganlian'

urlpatterns = [
    path('mobile/login', views.mobile_login, name='mobile_login'),
]
