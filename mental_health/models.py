from django.db import models
from django.contrib.auth.models import User


class MoodLog(models.Model):
    """Daily mood tracking entries."""
    
    MOOD_CHOICES = [
        (1, '😞 Very Low'),
        (2, '😔 Low'),
        (3, '😐 Okay'),
        (4, '🙂 Good'),
        (5, '😊 Great'),
        (6, '🤗 Excellent'),
        (7, '😄 Amazing'),
    ]
    
    ACTIVITY_CHOICES = [
        ('exercise', 'Exercise'),
        ('meditation', 'Meditation'),
        ('reading', 'Reading'),
        ('socializing', 'Socializing'),
        ('work', 'Work'),
        ('rest', 'Rest'),
        ('hobbies', 'Hobbies'),
        ('nature', 'Nature Walk'),
        ('yoga', 'Yoga'),
        ('journaling', 'Journaling'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mood_logs')
    date = models.DateField()
    mood_score = models.IntegerField(choices=MOOD_CHOICES)
    activities = models.CharField(max_length=500, blank=True, help_text='Comma-separated activities')
    sleep_hours = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    stress_level = models.IntegerField(default=5, help_text='1-10 scale')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    @property
    def mood_emoji(self):
        emojis = {1: '😞', 2: '😔', 3: '😐', 4: '🙂', 5: '😊', 6: '🤗', 7: '😄'}
        return emojis.get(self.mood_score, '😐')
    
    @property
    def mood_label(self):
        labels = {1: 'Very Low', 2: 'Low', 3: 'Okay', 4: 'Good', 5: 'Great', 6: 'Excellent', 7: 'Amazing'}
        return labels.get(self.mood_score, 'Unknown')
    
    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.mood_label}"
    
    class Meta:
        ordering = ['-date']
        unique_together = ['user', 'date']


class CounselingResource(models.Model):
    """Mental health resources and articles."""
    
    CATEGORY_CHOICES = [
        ('mindfulness', 'Mindfulness'),
        ('stress', 'Stress Management'),
        ('anxiety', 'Anxiety'),
        ('depression', 'Depression'),
        ('self_care', 'Self Care'),
        ('relationships', 'Relationships'),
        ('sleep', 'Sleep Health'),
        ('breathing', 'Breathing Exercises'),
    ]
    
    TYPE_CHOICES = [
        ('article', 'Article'),
        ('exercise', 'Exercise'),
        ('video', 'Video'),
        ('guide', 'Guide'),
    ]
    
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    resource_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='article')
    content = models.TextField()
    summary = models.TextField(max_length=300, blank=True)
    image = models.ImageField(upload_to='mental_health/', blank=True, null=True)
    external_link = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_featured = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-is_featured', '-created_at']
