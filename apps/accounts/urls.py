from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.AdminLoginView.as_view(), name='login'),
    path('logout/', views.admin_logout, name='logout'),
    path('users/', views.user_list, name='user_list'),
    path('users/create/', views.user_create, name='user_create'),
    path('users/<int:pk>/edit/', views.user_update, name='user_update'),
    path('users/<int:pk>/toggle-active/', views.user_toggle_active, name='user_toggle_active'),
]
