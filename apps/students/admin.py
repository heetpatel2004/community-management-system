from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'full_name', 'family', 'is_active']
    list_filter = ['is_active']
    search_fields = ['student_id', 'full_name', 'family__family_id', 'family__family_name']
    readonly_fields = ['student_id', 'created_at', 'updated_at']
