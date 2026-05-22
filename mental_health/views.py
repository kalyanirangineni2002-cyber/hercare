from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import MoodLog, CounselingResource
from .forms import MoodLogForm


@login_required
def mental_health_home(request):
    """Mental health overview page."""
    recent_moods = MoodLog.objects.filter(user=request.user)[:7]
    featured_resources = CounselingResource.objects.filter(is_featured=True)[:4]
    all_resources = CounselingResource.objects.all()[:8]
    
    # Check if already logged today
    today_logged = MoodLog.objects.filter(
        user=request.user,
        date=timezone.now().date()
    ).exists()
    
    context = {
        'recent_moods': recent_moods,
        'featured_resources': featured_resources,
        'all_resources': all_resources,
        'today_logged': today_logged,
    }
    return render(request, 'mental_health/mental_health.html', context)


@login_required
def log_mood(request):
    """Log daily mood."""
    today = timezone.now().date()
    
    # Check for existing entry
    existing = MoodLog.objects.filter(user=request.user, date=today).first()
    
    if request.method == 'POST':
        form = MoodLogForm(request.POST, instance=existing)
        if form.is_valid():
            mood = form.save(commit=False)
            mood.user = request.user
            mood.save()
            messages.success(request, 'Mood logged successfully! 💜')
            return redirect('mental_health_home')
    else:
        initial = {'date': today}
        form = MoodLogForm(instance=existing, initial=initial if not existing else None)
    
    context = {'form': form, 'editing': existing is not None}
    return render(request, 'mental_health/mood_log.html', context)


@login_required
def mood_history(request):
    """View mood history with trends."""
    moods = MoodLog.objects.filter(user=request.user).order_by('date')
    
    # Prepare chart data
    chart_data = {
        'labels': [m.date.strftime('%b %d') for m in moods[-30:]],
        'scores': [m.mood_score for m in moods[-30:]],
        'stress': [m.stress_level for m in moods[-30:]],
    }
    
    # Calculate averages
    if moods.exists():
        avg_mood = round(sum(m.mood_score for m in moods) / moods.count(), 1)
        avg_stress = round(sum(m.stress_level for m in moods) / moods.count(), 1)
        avg_sleep = None
        sleep_entries = [m for m in moods if m.sleep_hours]
        if sleep_entries:
            avg_sleep = round(sum(float(m.sleep_hours) for m in sleep_entries) / len(sleep_entries), 1)
    else:
        avg_mood = avg_stress = avg_sleep = None
    
    context = {
        'moods': moods.order_by('-date'),
        'chart_data': chart_data,
        'avg_mood': avg_mood,
        'avg_stress': avg_stress,
        'avg_sleep': avg_sleep,
    }
    return render(request, 'mental_health/mood_history.html', context)


@login_required
def resources(request):
    """Browse counseling resources."""
    category = request.GET.get('category', '')
    resource_type = request.GET.get('type', '')
    
    queryset = CounselingResource.objects.all()
    
    if category:
        queryset = queryset.filter(category=category)
    if resource_type:
        queryset = queryset.filter(resource_type=resource_type)
    
    context = {
        'resources': queryset,
        'categories': CounselingResource.CATEGORY_CHOICES,
        'types': CounselingResource.TYPE_CHOICES,
        'selected_category': category,
        'selected_type': resource_type,
    }
    return render(request, 'mental_health/resources.html', context)
