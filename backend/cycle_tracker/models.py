from django.db import models
from django.contrib.auth.models import User


class CycleLog(models.Model):
    """Tracks menstrual cycle entries."""
    
    FLOW_CHOICES = [
        ('light', 'Light'),
        ('medium', 'Medium'),
        ('heavy', 'Heavy'),
    ]
    
    SYMPTOM_CHOICES = [
        ('cramps', 'Cramps'),
        ('headache', 'Headache'),
        ('bloating', 'Bloating'),
        ('mood_swings', 'Mood Swings'),
        ('fatigue', 'Fatigue'),
        ('back_pain', 'Back Pain'),
        ('breast_tenderness', 'Breast Tenderness'),
        ('acne', 'Acne'),
        ('nausea', 'Nausea'),
        ('insomnia', 'Insomnia'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cycle_logs')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    cycle_length = models.IntegerField(null=True, blank=True, help_text='Days between this and next period')
    period_length = models.IntegerField(null=True, blank=True, help_text='Duration of period in days')
    flow_intensity = models.CharField(max_length=10, choices=FLOW_CHOICES, default='medium')
    symptoms = models.CharField(max_length=500, blank=True, help_text='Comma-separated symptoms')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        """Auto-calculate period length and cycle length."""
        if self.start_date and self.end_date:
            self.period_length = (self.end_date - self.start_date).days + 1
        
        # Calculate cycle length from previous entry
        if self.user_id:
            prev_log = CycleLog.objects.filter(
                user=self.user,
                start_date__lt=self.start_date
            ).order_by('-start_date').first()
            
            if prev_log:
                prev_log.cycle_length = (self.start_date - prev_log.start_date).days
                CycleLog.objects.filter(pk=prev_log.pk).update(
                    cycle_length=(self.start_date - prev_log.start_date).days
                )
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.user.username} - {self.start_date}"
    
    class Meta:
        ordering = ['-start_date']
        verbose_name = 'Cycle Log'
        verbose_name_plural = 'Cycle Logs'
