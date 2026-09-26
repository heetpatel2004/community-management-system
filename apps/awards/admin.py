from django.contrib import admin
from .models import AwardCategory, Award


@admin.register(AwardCategory)
class AwardCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    list_filter = ['is_active']


@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
    list_display = ['annual_registration', 'category', 'created_at']
    list_filter = ['category']
