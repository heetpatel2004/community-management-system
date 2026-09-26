from django.urls import path
from . import views

app_name = 'awards'

urlpatterns = [
    path('admin/categories/', views.admin_category_list, name='admin_category_list'),
    path('admin/categories/create/', views.admin_category_create, name='admin_category_create'),
    path('admin/categories/<int:pk>/edit/', views.admin_category_edit, name='admin_category_edit'),
    path('admin/', views.admin_award_list, name='admin_list'),
    path('admin/assign/<int:registration_pk>/', views.admin_award_create, name='admin_create'),
    path('admin/<int:pk>/delete/', views.admin_award_delete, name='admin_delete'),
]
