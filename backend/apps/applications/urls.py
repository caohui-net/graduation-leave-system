from django.urls import path
from . import views

urlpatterns = [
    path('', views.applications_view, name='applications'),
    path('<str:application_id>/', views.get_application, name='get_application'),
]
