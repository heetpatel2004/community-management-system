from django.urls import path
from . import views

app_name = 'registrations'

urlpatterns = [
    # Public
    path('submit/<str:family_id>/<int:student_pk>/', views.public_register, name='public_register'),
    path('edit/<str:family_id>/<int:pk>/', views.public_edit_registration, name='public_edit'),

    # Admin
    path('admin/', views.admin_registration_list, name='admin_list'),
    path('admin/<int:pk>/', views.admin_registration_detail, name='admin_detail'),
    path('admin/<int:pk>/edit/', views.admin_registration_edit, name='admin_edit'),
    path('admin/<int:pk>/verify/<str:action>/', views.admin_registration_verify, name='admin_verify'),
]
