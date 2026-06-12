from django.urls import path
from . import views

urlpatterns = [
    path('', views.applications_view, name='applications'),
    path('stats/', views.get_stats, name='application_stats'),
    path('draft/', views.get_or_create_draft, name='create_draft'),
    path('<str:application_id>/', views.get_application, name='get_application'),
]
