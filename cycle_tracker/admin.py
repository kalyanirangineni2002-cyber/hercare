from django.contrib import admin
from .models import CycleLog

@admin.register(CycleLog)
class CycleLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'start_date', 'end_date', 'cycle_length', 'period_length', 'flow_intensity']
    list_filter = ['flow_intensity', 'start_date']
    search_fields = ['user__username']
