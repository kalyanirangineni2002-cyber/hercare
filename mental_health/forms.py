from django import forms
from .models import MoodLog


class MoodLogForm(forms.ModelForm):
    """Form for logging daily mood."""
    
    ACTIVITY_CHOICES = [
        ('exercise', 'Exercise'),
        ('meditation', 'Meditation'),
        ('reading', 'Reading'),
        ('socializing', 'Socializing'),
        ('work', 'Work'),
        ('rest', 'Rest'),
        ('hobbies', 'Hobbies'),
        ('nature', 'Nature Walk'),
        ('yoga', 'Yoga'),
        ('journaling', 'Journaling'),
    ]
    
    activities_list = forms.MultipleChoiceField(
        choices=ACTIVITY_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'activity-checkbox'}),
        label='Activities Today'
    )
    
    class Meta:
        model = MoodLog
        fields = ['date', 'mood_score', 'sleep_hours', 'stress_level', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'mood_score': forms.RadioSelect(attrs={'class': 'mood-radio'}),
            'sleep_hours': forms.NumberInput(attrs={
                'class': 'form-control', 'step': '0.5', 'min': '0', 'max': '24',
                'placeholder': 'Hours slept'
            }),
            'stress_level': forms.NumberInput(attrs={
                'class': 'form-control', 'type': 'range', 'min': '1', 'max': '10',
                'step': '1'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 3,
                'placeholder': 'How are you feeling today?'
            }),
        }
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        activities = self.cleaned_data.get('activities_list', [])
        instance.activities = ','.join(activities)
        if commit:
            instance.save()
        return instance
