from django.db import models
from django.contrib.auth.models import User


class Doctor(models.Model):
    """Doctor profiles for consultations."""
    
    SPECIALIZATION_CHOICES = [
        ('gynecologist', 'Gynecologist'),
        ('obstetrician', 'Obstetrician'),
        ('dermatologist', 'Dermatologist'),
        ('endocrinologist', 'Endocrinologist'),
        ('nutritionist', 'Nutritionist'),
        ('psychiatrist', 'Psychiatrist'),
        ('psychologist', 'Psychologist'),
        ('general', 'General Physician'),
        ('physiotherapist', 'Physiotherapist'),
    ]
    
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=20, choices=SPECIALIZATION_CHOICES)
    qualification = models.CharField(max_length=200)
    experience_years = models.IntegerField(default=0)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=4.0)
    consultation_fee = models.DecimalField(max_digits=8, decimal_places=2)
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='doctors/', blank=True, null=True)
    available_days = models.CharField(max_length=100, default='Mon,Tue,Wed,Thu,Fri',
                                       help_text='Comma-separated days')
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Dr. {self.name} ({self.get_specialization_display()})"
    
    class Meta:
        ordering = ['-rating', 'name']


class TimeSlot(models.Model):
    """Available time slots for doctors."""
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='time_slots')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_booked = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.doctor.name} - {self.date} {self.start_time}-{self.end_time}"
    
    class Meta:
        ordering = ['date', 'start_time']
        unique_together = ['doctor', 'date', 'start_time']


class Appointment(models.Model):
    """User appointments with doctors."""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    time_slot = models.OneToOneField(TimeSlot, on_delete=models.CASCADE, related_name='appointment')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    reason = models.TextField(blank=True, help_text='Reason for visit')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} → Dr. {self.doctor.name} on {self.time_slot.date}"
    
    class Meta:
        ordering = ['-created_at']
