from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_approvals, name='list_approvals'),
    path('<str:approval_id>/approve/', views.approve_approval, name='approve_approval'),
    path('<str:approval_id>/reject/', views.reject_approval, name='reject_approval'),
]
