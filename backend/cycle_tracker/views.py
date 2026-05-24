from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from datetime import timedelta
from .models import CycleLog
from .forms import CycleLogForm


@login_required
def tracker_home(request):
    """Main cycle tracker page with calendar and history."""
    logs = CycleLog.objects.filter(user=request.user).order_by('-start_date')
    
    # Calculate average cycle length
    cycles_with_length = logs.filter(cycle_length__isnull=False)
    avg_cycle = None
    if cycles_with_length.exists():
        avg_cycle = round(sum(c.cycle_length for c in cycles_with_length) / cycles_with_length.count())
    
    # Predict next period
    next_period = None
    latest = logs.first()
    if latest:
        cycle_len = avg_cycle or 28
        next_period = latest.start_date + timedelta(days=cycle_len)
    
    # Prepare calendar data as JSON
    calendar_data = []
    for log in logs:
        entry = {
            'start': log.start_date.isoformat(),
            'end': log.end_date.isoformat() if log.end_date else log.start_date.isoformat(),
            'flow': log.flow_intensity,
        }
        calendar_data.append(entry)
    
    context = {
        'logs': logs[:12],
        'avg_cycle': avg_cycle,
        'next_period': next_period,
        'calendar_data': calendar_data,
        'latest': latest,
    }
    return render(request, 'cycle_tracker/tracker.html', context)


@login_required
def log_period(request):
    """Log a new period entry."""
    if request.method == 'POST':
        form = CycleLogForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.user = request.user
            log.save()
            messages.success(request, 'Period logged successfully!')
            return redirect('tracker_home')
    else:
        form = CycleLogForm()
    
    return render(request, 'cycle_tracker/log_form.html', {'form': form})


@login_required
def cycle_history(request):
    """View cycle history with analytics."""
    logs = CycleLog.objects.filter(user=request.user).order_by('-start_date')
    
    # Analytics
    total_logs = logs.count()
    cycles_with_length = logs.filter(cycle_length__isnull=False)
    avg_cycle = None
    avg_period = None
    
    if cycles_with_length.exists():
        avg_cycle = round(sum(c.cycle_length for c in cycles_with_length) / cycles_with_length.count())
    
    periods_with_length = logs.filter(period_length__isnull=False)
    if periods_with_length.exists():
        avg_period = round(sum(p.period_length for p in periods_with_length) / periods_with_length.count())
    
    # Symptom frequency
    symptom_counts = {}
    for log in logs:
        if log.symptoms:
            for symptom in log.symptoms.split(','):
                symptom = symptom.strip()
                if symptom:
                    symptom_counts[symptom] = symptom_counts.get(symptom, 0) + 1
    
    context = {
        'logs': logs,
        'total_logs': total_logs,
        'avg_cycle': avg_cycle,
        'avg_period': avg_period,
        'symptom_counts': dict(sorted(symptom_counts.items(), key=lambda x: x[1], reverse=True)),
    }
    return render(request, 'cycle_tracker/history.html', context)


@login_required
def delete_cycle_log(request, pk):
    """Delete a cycle log entry."""
    log = get_object_or_404(CycleLog, pk=pk, user=request.user)
    if request.method == 'POST':
        log.delete()
        messages.success(request, 'Cycle log deleted.')
    return redirect('tracker_home')
