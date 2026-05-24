from django.contrib import admin
from .models import Doctor, TimeSlot, Appointment

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['name', 'specialization', 'experience_years', 'rating', 'consultation_fee', 'is_active']
    list_filter = ['specialization', 'is_active']
    search_fields = ['name', 'qualification']

@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'date', 'start_time', 'end_time', 'is_booked']
    list_filter = ['is_booked', 'date']

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'doctor', 'time_slot', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['user__username', 'doctor__name']
