from django import forms
from .models import MedicineReminder


class MedicineReminderForm(forms.ModelForm):
    """Form for creating/editing medicine reminders."""
    class Meta:
        model = MedicineReminder
        fields = ['medicine_name', 'dosage', 'frequency', 'time_morning',
                  'time_afternoon', 'time_evening', 'start_date', 'end_date', 'notes']
        widgets = {
            'medicine_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Medicine name'}),
            'dosage': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 500mg, 1 tablet'}),
            'frequency': forms.Select(attrs={'class': 'form-control'}),
            'time_morning': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'time_afternoon': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'time_evening': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Instructions...'}),
        }
