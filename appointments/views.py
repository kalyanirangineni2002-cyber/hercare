from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Doctor, TimeSlot, Appointment
from .forms import AppointmentForm


@login_required
def doctor_list(request):
    """Browse doctors with optional specialization filter."""
    specialization = request.GET.get('specialization', '')
    doctors = Doctor.objects.filter(is_active=True)
    
    if specialization:
        doctors = doctors.filter(specialization=specialization)
    
    specializations = Doctor.SPECIALIZATION_CHOICES
    
    context = {
        'doctors': doctors,
        'specializations': specializations,
        'selected_spec': specialization,
    }
    return render(request, 'appointments/doctors.html', context)


@login_required
def doctor_detail(request, pk):
    """Doctor profile with available time slots."""
    doctor = get_object_or_404(Doctor, pk=pk, is_active=True)
    today = timezone.now().date()
    
    available_slots = TimeSlot.objects.filter(
        doctor=doctor,
        date__gte=today,
        is_booked=False
    ).order_by('date', 'start_time')
    
    # Group slots by date
    slots_by_date = {}
    for slot in available_slots:
        date_str = slot.date.strftime('%A, %B %d, %Y')
        if date_str not in slots_by_date:
            slots_by_date[date_str] = []
        slots_by_date[date_str].append(slot)
    
    context = {
        'doctor': doctor,
        'slots_by_date': slots_by_date,
    }
    return render(request, 'appointments/doctor_detail.html', context)


@login_required
def book_appointment(request, slot_id):
    """Book a specific time slot."""
    slot = get_object_or_404(TimeSlot, pk=slot_id, is_booked=False)
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user
            appointment.doctor = slot.doctor
            appointment.time_slot = slot
            appointment.save()
            
            slot.is_booked = True
            slot.save()
            
            messages.success(request, f'Appointment booked with Dr. {slot.doctor.name} on {slot.date}!')
            return redirect('my_appointments')
    else:
        form = AppointmentForm()
    
    context = {
        'form': form,
        'slot': slot,
        'doctor': slot.doctor,
    }
    return render(request, 'appointments/book.html', context)


@login_required
def my_appointments(request):
    """View user's appointments."""
    appointments = Appointment.objects.filter(user=request.user).select_related(
        'doctor', 'time_slot'
    ).order_by('-time_slot__date')
    
    upcoming = appointments.filter(
        time_slot__date__gte=timezone.now().date(),
        status__in=['pending', 'confirmed']
    )
    past = appointments.filter(
        time_slot__date__lt=timezone.now().date()
    ) | appointments.filter(status__in=['completed', 'cancelled'])
    
    context = {
        'upcoming': upcoming,
        'past': past.distinct(),
    }
    return render(request, 'appointments/my_appointments.html', context)


@login_required
def cancel_appointment(request, pk):
    """Cancel an appointment."""
    appointment = get_object_or_404(Appointment, pk=pk, user=request.user)
    
    if request.method == 'POST':
        appointment.status = 'cancelled'
        appointment.save()
        
        # Free the time slot
        appointment.time_slot.is_booked = False
        appointment.time_slot.save()
        
        messages.success(request, 'Appointment cancelled successfully.')
    
    return redirect('my_appointments')
