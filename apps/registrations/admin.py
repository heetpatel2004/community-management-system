from django.contrib import admin
from .models import AnnualRegistration


@admin.register(AnnualRegistration)
class AnnualRegistrationAdmin(admin.ModelAdmin):
    list_display = ['student', 'event', 'standard', 'medium', 'percentage_or_cgpa', 'status']
    list_filter = ['status', 'medium', 'event']
    search_fields = ['student__student_id', 'student__full_name']
    readonly_fields = ['submitted_at', 'verified_at', 'created_at', 'updated_at']
