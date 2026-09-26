from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('admin/', views.admin_event_list, name='admin_list'),
    path('admin/create/', views.admin_event_create, name='admin_create'),
    path('admin/<int:pk>/edit/', views.admin_event_edit, name='admin_edit'),
    path('admin/<int:pk>/status/<str:new_status>/', views.admin_event_change_status, name='admin_change_status'),
]
