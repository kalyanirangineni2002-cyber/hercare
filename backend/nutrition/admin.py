from django.contrib import admin
from .models import NutritionArticle, FitnessRoutine, DailyTip

@admin.register(NutritionArticle)
class NutritionArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'is_featured', 'created_at']
    list_filter = ['category', 'is_featured']
    search_fields = ['title', 'content']

@admin.register(FitnessRoutine)
class FitnessRoutineAdmin(admin.ModelAdmin):
    list_display = ['title', 'difficulty', 'target_area', 'duration_minutes']
    list_filter = ['difficulty', 'target_area']

@admin.register(DailyTip)
class DailyTipAdmin(admin.ModelAdmin):
    list_display = ['tip_text', 'category', 'date_published']
    list_filter = ['category']
