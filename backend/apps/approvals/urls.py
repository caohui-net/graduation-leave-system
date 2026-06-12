from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_approvals, name='list_approvals'),
    path('statistics/', views.get_statistics, name='get_statistics'),
    path('export/', views.export_approvals, name='export_approvals'),
    path('batch-action/', views.batch_action_approvals, name='batch_action_approvals'),
    path('<str:approval_id>/', views.get_approval, name='get_approval'),
    path('<str:approval_id>/approve/', views.approve_approval, name='approve_approval'),
    path('<str:approval_id>/reject/', views.reject_approval, name='reject_approval'),
]
