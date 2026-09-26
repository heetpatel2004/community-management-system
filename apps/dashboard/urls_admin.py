from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='admin_home'),
    path('search/', views.admin_search, name='search'),
]
