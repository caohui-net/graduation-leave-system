from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_notifications, name='notification-list'),
    path('unread_count/', views.unread_count, name='notification-unread-count'),
    path('<str:notification_id>/read/', views.mark_as_read, name='notification-mark-read'),
    path('mark_all_read/', views.mark_all_read, name='notification-mark-all-read'),
]
