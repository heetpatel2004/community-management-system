from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('admin/', views.report_view, name='report'),
]
