from django.db import models
from django.contrib.auth.models import User
import os

class HealthReport(models.Model):
    """Stores user-uploaded medical and health reports."""
    
    REPORT_TYPE_CHOICES = [
        ('blood_test', 'Blood Test / Lab Report'),
        ('prescription', 'Prescription'),
        ('scan', 'Ultrasound / X-Ray / Scan'),
        ('vaccine', 'Vaccination Record'),
        ('discharge', 'Discharge Summary'),
        ('other', 'Other Document'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='health_reports')
    title = models.CharField(max_length=200)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPE_CHOICES, default='other')
    file = models.FileField(upload_to='health_reports/%Y/%m/%d/')
    upload_date = models.DateField(auto_now_add=True)
    report_date = models.DateField(help_text="Date on the report/document")
    doctor_name = models.CharField(max_length=150, blank=True, help_text="Prescribing or consulting doctor")
    hospital_clinic = models.CharField(max_length=200, blank=True, help_text="Hospital or diagnostic clinic")
    notes = models.TextField(blank=True, help_text="Brief notes or diagnosis summary")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} - {self.user.username} ({self.get_report_type_display()})"
    
    @property
    def file_name(self):
        return os.path.basename(self.file.name)
        
    @property
    def file_extension(self):
        name, ext = os.path.splitext(self.file.name)
        return ext.lower().replace('.', '')
        
    class Meta:
        ordering = ['-report_date', '-created_at']
        verbose_name = 'Health Report'
        verbose_name_plural = 'Health Reports'
