from django.contrib import admin
from .models import Family


@admin.register(Family)
class FamilyAdmin(admin.ModelAdmin):
    list_display = ['family_id', 'family_name', 'responsible_person_name', 'mobile_number', 'village_city', 'is_active']
    list_filter = ['is_active', 'village_city']
    search_fields = ['family_id', 'family_name', 'responsible_person_name', 'mobile_number', 'village_city']
    readonly_fields = ['family_id', 'created_at', 'updated_at']
