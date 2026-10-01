from django.urls import path
from . import views

app_name = 'families'

urlpatterns = [
    # Public
    path('register/', views.family_register, name='register'),
    path('lookup/', views.family_lookup, name='lookup'),
    path('<str:family_id>/', views.family_portal, name='portal'),
    path('<str:family_id>/edit-student/<int:student_pk>/', views.family_edit_student, name='edit_student'),
    path('<str:family_id>/add-student/', views.family_add_student, name='add_student'),

    # Admin
    path('admin/', views.admin_family_list, name='admin_list'),
    path('admin/<int:pk>/', views.admin_family_detail, name='admin_detail'),
    path('admin/<int:pk>/edit/', views.admin_family_edit, name='admin_edit'),
    path('admin/<int:pk>/add-student/', views.admin_family_add_student, name='admin_add_student'),
]
