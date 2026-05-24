from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta


@login_required
def dashboard_view(request):
    """Main dashboard with health summary widgets."""
    user = request.user
    today = timezone.now().date()
    
    # Get upcoming appointments
    upcoming_appointments = []
    try:
        from appointments.models import Appointment
        upcoming_appointments = Appointment.objects.filter(
            user=user,
            time_slot__date__gte=today,
            status__in=['pending', 'confirmed']
        ).select_related('doctor', 'time_slot').order_by('time_slot__date', 'time_slot__start_time')[:3]
    except Exception:
        pass
    
    # Get today's medicine reminders
    todays_reminders = []
    try:
        from reminders.models import MedicineReminder
        todays_reminders = MedicineReminder.objects.filter(
            user=user,
            is_active=True,
            start_date__lte=today,
        ).filter(
            models__isnull=True
        )[:5]
    except Exception:
        try:
            from reminders.models import MedicineReminder
            todays_reminders = MedicineReminder.objects.filter(
                user=user,
                is_active=True,
            )[:5]
        except Exception:
            pass
    
    # Get latest cycle info
    latest_cycle = None
    next_period = None
    days_until_period = None
    try:
        from cycle_tracker.models import CycleLog
        latest_cycle = CycleLog.objects.filter(user=user).order_by('-start_date').first()
        if latest_cycle and latest_cycle.cycle_length:
            next_period = latest_cycle.start_date + timedelta(days=latest_cycle.cycle_length)
            days_until_period = (next_period - today).days
    except Exception:
        pass
    
    # Get latest mood
    latest_mood = None
    try:
        from mental_health.models import MoodLog
        latest_mood = MoodLog.objects.filter(user=user).order_by('-date').first()
    except Exception:
        pass
    
    # Get health reports count
    reports_count = 0
    try:
        from health_reports.models import HealthReport
        reports_count = HealthReport.objects.filter(user=user).count()
    except Exception:
        pass
    
    context = {
        'upcoming_appointments': upcoming_appointments,
        'todays_reminders': todays_reminders,
        'latest_cycle': latest_cycle,
        'next_period': next_period,
        'days_until_period': days_until_period,
        'latest_mood': latest_mood,
        'reports_count': reports_count,
        'today': today,
    }
    return render(request, 'dashboard/dashboard.html', context)
