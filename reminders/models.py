from django.db import models
from django.contrib.auth.models import User
import json


class MedicineReminder(models.Model):
    """Medicine reminder entries."""
    
    FREQUENCY_CHOICES = [
        ('once_daily', 'Once Daily'),
        ('twice_daily', 'Twice Daily'),
        ('three_daily', 'Three Times Daily'),
        ('weekly', 'Weekly'),
        ('as_needed', 'As Needed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reminders')
    medicine_name = models.CharField(max_length=200)
    dosage = models.CharField(max_length=100, help_text='e.g., 500mg, 1 tablet')
    frequency = models.CharField(max_length=15, choices=FREQUENCY_CHOICES, default='once_daily')
    time_morning = models.TimeField(null=True, blank=True)
    time_afternoon = models.TimeField(null=True, blank=True)
    time_evening = models.TimeField(null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True, help_text='Instructions or notes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.medicine_name} ({self.dosage}) - {self.user.username}"
    
    @property
    def time_slots_display(self):
        slots = []
        if self.time_morning:
            slots.append(f"Morning: {self.time_morning.strftime('%I:%M %p')}")
        if self.time_afternoon:
            slots.append(f"Afternoon: {self.time_afternoon.strftime('%I:%M %p')}")
        if self.time_evening:
            slots.append(f"Evening: {self.time_evening.strftime('%I:%M %p')}")
        return slots
    
    class Meta:
        ordering = ['-is_active', '-created_at']


class MedicineLog(models.Model):
    """Track when medicine was taken."""
    reminder = models.ForeignKey(MedicineReminder, on_delete=models.CASCADE, related_name='logs')
    taken_at = models.DateTimeField(auto_now_add=True)
    taken_date = models.DateField()
    time_slot = models.CharField(max_length=10, choices=[
        ('morning', 'Morning'),
        ('afternoon', 'Afternoon'),
        ('evening', 'Evening'),
    ])
    
    def __str__(self):
        return f"{self.reminder.medicine_name} taken on {self.taken_date}"
    
    class Meta:
        ordering = ['-taken_at']
        unique_together = ['reminder', 'taken_date', 'time_slot']
