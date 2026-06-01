from django.urls import path
from . import views

urlpatterns = [
    path('applications/<str:application_id>/attachments/', views.attachments_view, name='attachments'),
    path('attachments/<str:attachment_id>/download/', views.download_attachment, name='download_attachment'),
    path('attachments/<str:attachment_id>/', views.delete_attachment, name='delete_attachment'),
]
