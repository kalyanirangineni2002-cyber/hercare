from django.contrib import admin
from .models import HealthReport

@admin.register(HealthReport)
class HealthReportAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'report_type', 'report_date', 'upload_date']
    list_filter = ['report_type', 'report_date', 'upload_date']
    search_fields = ['title', 'user__username', 'doctor_name', 'hospital_clinic', 'notes']
