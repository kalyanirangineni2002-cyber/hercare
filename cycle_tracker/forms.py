from django import forms
from .models import CycleLog


class CycleLogForm(forms.ModelForm):
    """Form for logging a menstrual cycle entry."""
    
    SYMPTOM_CHOICES = [
        ('cramps', 'Cramps'),
        ('headache', 'Headache'),
        ('bloating', 'Bloating'),
        ('mood_swings', 'Mood Swings'),
        ('fatigue', 'Fatigue'),
        ('back_pain', 'Back Pain'),
        ('breast_tenderness', 'Breast Tenderness'),
        ('acne', 'Acne'),
        ('nausea', 'Nausea'),
        ('insomnia', 'Insomnia'),
    ]
    
    symptoms_list = forms.MultipleChoiceField(
        choices=SYMPTOM_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'symptom-checkbox'}),
        label='Symptoms'
    )
    
    class Meta:
        model = CycleLog
        fields = ['start_date', 'end_date', 'flow_intensity', 'notes']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'flow_intensity': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Any additional notes...'}),
        }
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        symptoms = self.cleaned_data.get('symptoms_list', [])
        instance.symptoms = ','.join(symptoms)
        if commit:
            instance.save()
        return instance
