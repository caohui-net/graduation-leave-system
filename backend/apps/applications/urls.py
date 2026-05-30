from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_application, name='create_application'),
    path('<str:application_id>/', views.get_application, name='get_application'),
]
