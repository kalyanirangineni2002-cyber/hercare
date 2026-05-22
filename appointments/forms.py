from django import forms
from .models import Appointment


class AppointmentForm(forms.ModelForm):
    """Form for booking an appointment."""
    class Meta:
        model = Appointment
        fields = ['reason', 'notes']
        widgets = {
            'reason': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe the reason for your visit...'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Any additional notes for the doctor...'
            }),
        }
