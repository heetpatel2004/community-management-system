"""
Forms for Award management.
"""

from django import forms
from .models import AwardCategory, Award


class AwardCategoryForm(forms.ModelForm):
    """Form for creating/editing award categories."""

    class Meta:
        model = AwardCategory
        fields = ['name', 'description', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Academic Excellence',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
            }),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class AwardForm(forms.ModelForm):
    """Form for assigning an award to a registration."""

    class Meta:
        model = Award
        fields = ['category', 'remarks']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'remarks': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Additional remarks (optional)',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = AwardCategory.objects.filter(is_active=True)
