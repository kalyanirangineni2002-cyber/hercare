from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import NutritionArticle, FitnessRoutine, DailyTip


@login_required
def nutrition_home(request):
    """Nutrition overview with daily tip and featured content."""
    daily_tip = DailyTip.objects.first()
    featured_articles = NutritionArticle.objects.filter(is_featured=True)[:3]
    recent_articles = NutritionArticle.objects.all()[:6]
    popular_routines = FitnessRoutine.objects.all()[:4]
    
    context = {
        'daily_tip': daily_tip,
        'featured_articles': featured_articles,
        'recent_articles': recent_articles,
        'popular_routines': popular_routines,
    }
    return render(request, 'nutrition/nutrition.html', context)


@login_required
def article_detail(request, pk):
    """View full article."""
    article = get_object_or_404(NutritionArticle, pk=pk)
    related = NutritionArticle.objects.filter(category=article.category).exclude(pk=pk)[:3]
    
    context = {
        'article': article,
        'related': related,
    }
    return render(request, 'nutrition/article.html', context)


@login_required
def fitness_routines(request):
    """Browse fitness routines."""
    difficulty = request.GET.get('difficulty', '')
    target = request.GET.get('target', '')
    
    routines = FitnessRoutine.objects.all()
    
    if difficulty:
        routines = routines.filter(difficulty=difficulty)
    if target:
        routines = routines.filter(target_area=target)
    
    context = {
        'routines': routines,
        'difficulties': FitnessRoutine.DIFFICULTY_CHOICES,
        'targets': FitnessRoutine.TARGET_CHOICES,
        'selected_difficulty': difficulty,
        'selected_target': target,
    }
    return render(request, 'nutrition/fitness.html', context)


@login_required
def routine_detail(request, pk):
    """View routine details."""
    routine = get_object_or_404(FitnessRoutine, pk=pk)
    
    context = {'routine': routine}
    return render(request, 'nutrition/routine_detail.html', context)
