from django.db import models


class NutritionArticle(models.Model):
    """Nutrition tips and articles."""
    
    CATEGORY_CHOICES = [
        ('diet', 'Diet & Nutrition'),
        ('recipes', 'Healthy Recipes'),
        ('supplements', 'Supplements'),
        ('hydration', 'Hydration'),
        ('weight', 'Weight Management'),
        ('hormonal', 'Hormonal Health Diet'),
        ('pregnancy', 'Pregnancy Nutrition'),
        ('pcos', 'PCOS Diet'),
    ]
    
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    content = models.TextField()
    summary = models.TextField(max_length=300, blank=True)
    image = models.ImageField(upload_to='nutrition/', blank=True, null=True)
    tags = models.CharField(max_length=200, blank=True, help_text='Comma-separated tags')
    created_at = models.DateTimeField(auto_now_add=True)
    is_featured = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-is_featured', '-created_at']


class FitnessRoutine(models.Model):
    """Fitness routines and exercise plans."""
    
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    TARGET_CHOICES = [
        ('full_body', 'Full Body'),
        ('core', 'Core & Abs'),
        ('upper_body', 'Upper Body'),
        ('lower_body', 'Lower Body'),
        ('flexibility', 'Flexibility'),
        ('cardio', 'Cardio'),
        ('yoga', 'Yoga'),
        ('pelvic', 'Pelvic Floor'),
    ]
    
    title = models.CharField(max_length=200)
    difficulty = models.CharField(max_length=15, choices=DIFFICULTY_CHOICES)
    target_area = models.CharField(max_length=15, choices=TARGET_CHOICES)
    duration_minutes = models.IntegerField(default=30)
    description = models.TextField()
    exercises = models.TextField(help_text='Exercise details with sets/reps')
    image = models.ImageField(upload_to='fitness/', blank=True, null=True)
    calories_burned = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} ({self.get_difficulty_display()})"
    
    class Meta:
        ordering = ['difficulty', 'title']


class DailyTip(models.Model):
    """Daily health and wellness tips."""
    
    CATEGORY_CHOICES = [
        ('nutrition', 'Nutrition'),
        ('fitness', 'Fitness'),
        ('wellness', 'Wellness'),
        ('mental_health', 'Mental Health'),
    ]
    
    tip_text = models.TextField(max_length=500)
    category = models.CharField(max_length=15, choices=CATEGORY_CHOICES)
    date_published = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.tip_text[:50]
    
    class Meta:
        ordering = ['-date_published']
