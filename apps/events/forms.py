"""
Forms for Event management.
"""

from django import forms
from .models import Event


class EventForm(forms.ModelForm):
    """Admin form for creating and editing events."""

    class Meta:
        model = Event
        fields = [
            'event_name', 'academic_year', 'event_date',
            'registration_start_date', 'registration_end_date', 'status',
        ]
        widgets = {
            'event_name': forms.TextInput(attrs={'class': 'form-control'}),
            'academic_year': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 2026-27',
            }),
            'event_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'registration_start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'registration_end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_academic_year(self):
        year = self.cleaned_data['academic_year'].strip()
        # Basic validation: should be like "2026-27"
        if len(year) < 4:
            raise forms.ValidationError('Please enter a valid academic year (e.g., 2026-27).')
        return year

    def clean(self):
        cleaned = super().clean()
        start = cleaned.get('registration_start_date')
        end = cleaned.get('registration_end_date')
        if start and end and start > end:
            raise forms.ValidationError('Registration start date must be before end date.')
        return cleaned
