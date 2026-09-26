from django.contrib import admin
from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['academic_year', 'event_name', 'event_date', 'status']
    list_filter = ['status']
    search_fields = ['academic_year']
