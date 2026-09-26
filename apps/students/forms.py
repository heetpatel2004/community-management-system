"""
Forms for Student management.
"""

from django import forms
from .models import Student


class StudentForm(forms.ModelForm):
    """Form for adding a student to a family."""

    class Meta:
        model = Student
        fields = ['full_name']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Rahul Patel',
            }),
        }
        labels = {
            'full_name': 'Student Full Name',
        }


class StudentEditForm(forms.ModelForm):
    """Admin form for editing student details."""

    class Meta:
        model = Student
        fields = ['full_name', 'is_active']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
