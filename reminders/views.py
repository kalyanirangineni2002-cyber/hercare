from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from .models import MedicineReminder, MedicineLog
from .forms import MedicineReminderForm


@login_required
def reminders_home(request):
    """View all reminders and today's schedule."""
    today = timezone.now().date()
    active_reminders = MedicineReminder.objects.filter(
        user=request.user, is_active=True
    )
    inactive_reminders = MedicineReminder.objects.filter(
        user=request.user, is_active=False
    )
    
    # Get today's logs
    todays_logs = MedicineLog.objects.filter(
        reminder__user=request.user,
        taken_date=today
    ).values_list('reminder_id', 'time_slot')
    
    taken_set = set()
    for reminder_id, time_slot in todays_logs:
        taken_set.add(f"{reminder_id}_{time_slot}")
    
    context = {
        'active_reminders': active_reminders,
        'inactive_reminders': inactive_reminders,
        'today': today,
        'taken_set': taken_set,
    }
    return render(request, 'reminders/reminders.html', context)


@login_required
def add_reminder(request):
    """Add a new medicine reminder."""
    if request.method == 'POST':
        form = MedicineReminderForm(request.POST)
        if form.is_valid():
            reminder = form.save(commit=False)
            reminder.user = request.user
            reminder.save()
            messages.success(request, f'Reminder for {reminder.medicine_name} added!')
            return redirect('reminders_home')
    else:
        form = MedicineReminderForm()
    
    return render(request, 'reminders/reminder_form.html', {'form': form, 'action': 'Add'})


@login_required
def edit_reminder(request, pk):
    """Edit an existing reminder."""
    reminder = get_object_or_404(MedicineReminder, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = MedicineReminderForm(request.POST, instance=reminder)
        if form.is_valid():
            form.save()
            messages.success(request, 'Reminder updated!')
            return redirect('reminders_home')
    else:
        form = MedicineReminderForm(instance=reminder)
    
    return render(request, 'reminders/reminder_form.html', {'form': form, 'action': 'Edit'})


@login_required
def delete_reminder(request, pk):
    """Delete a reminder."""
    reminder = get_object_or_404(MedicineReminder, pk=pk, user=request.user)
    if request.method == 'POST':
        name = reminder.medicine_name
        reminder.delete()
        messages.success(request, f'Reminder for {name} deleted.')
    return redirect('reminders_home')


@login_required
def toggle_reminder(request, pk):
    """Toggle reminder active/inactive."""
    reminder = get_object_or_404(MedicineReminder, pk=pk, user=request.user)
    reminder.is_active = not reminder.is_active
    reminder.save()
    status = 'activated' if reminder.is_active else 'deactivated'
    messages.success(request, f'Reminder {status}.')
    return redirect('reminders_home')


@login_required
def mark_taken(request, pk, time_slot):
    """Mark medicine as taken via AJAX."""
    reminder = get_object_or_404(MedicineReminder, pk=pk, user=request.user)
    today = timezone.now().date()
    
    log, created = MedicineLog.objects.get_or_create(
        reminder=reminder,
        taken_date=today,
        time_slot=time_slot,
    )
    
    if not created:
        # Already taken, untoggle
        log.delete()
        return JsonResponse({'status': 'unmarked', 'message': f'{reminder.medicine_name} unmarked for {time_slot}'})
    
    return JsonResponse({'status': 'marked', 'message': f'{reminder.medicine_name} marked as taken!'})
