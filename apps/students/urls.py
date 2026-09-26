from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('admin/', views.admin_student_list, name='admin_list'),
    path('admin/<int:pk>/', views.admin_student_detail, name='admin_detail'),
    path('admin/<int:pk>/edit/', views.admin_student_edit, name='admin_edit'),
]
