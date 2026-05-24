from django.contrib import admin
from .models import MedicineReminder, MedicineLog

@admin.register(MedicineReminder)
class MedicineReminderAdmin(admin.ModelAdmin):
    list_display = ['medicine_name', 'user', 'dosage', 'frequency', 'is_active', 'start_date']
    list_filter = ['is_active', 'frequency']
    search_fields = ['medicine_name', 'user__username']

@admin.register(MedicineLog)
class MedicineLogAdmin(admin.ModelAdmin):
    list_display = ['reminder', 'taken_date', 'time_slot', 'taken_at']
    list_filter = ['time_slot', 'taken_date']
