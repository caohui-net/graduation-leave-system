from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('demo-login', views.demo_login, name='demo_login'),
]
