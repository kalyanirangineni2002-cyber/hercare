from django import forms
from .models import HealthReport

class HealthReportForm(forms.ModelForm):
    """Form to upload and describe health reports."""
    class Meta:
        model = HealthReport
        fields = ['title', 'report_type', 'file', 'report_date', 'doctor_name', 'hospital_clinic', 'notes']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Annual Blood Panel 2026'}),
            'report_type': forms.Select(attrs={'class': 'form-select'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'report_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'doctor_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dr. Name (Optional)'}),
            'hospital_clinic': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Clinic/Hospital Name (Optional)'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Summarize findings or doctors instructions...'}),
        }
