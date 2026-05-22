from django.contrib import admin
from .models import MoodLog, CounselingResource

@admin.register(MoodLog)
class MoodLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'mood_score', 'stress_level', 'sleep_hours']
    list_filter = ['mood_score', 'date']

@admin.register(CounselingResource)
class CounselingResourceAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'resource_type', 'is_featured']
    list_filter = ['category', 'resource_type', 'is_featured']
    search_fields = ['title', 'content']
