"""
Forms for Annual Registration.
"""

from django import forms
from .models import AnnualRegistration
from .validators import validate_result_document


class AnnualRegistrationForm(forms.ModelForm):
    """Public form for yearly student registration."""

    result_document = forms.FileField(
        required=False,
        validators=[validate_result_document],
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control',
            'accept': '.pdf,.jpg,.jpeg,.png',
        }),
        help_text='Upload result document (PDF, JPG, PNG — max 5MB)',
    )

    class Meta:
        model = AnnualRegistration
        fields = ['standard', 'medium', 'percentage_or_cgpa', 'special_achievement', 'result_document']
        widgets = {
            'standard': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 10, 11, 12, B.Com Sem-1',
            }),
            'medium': forms.Select(attrs={'class': 'form-select'}),
            'percentage_or_cgpa': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 91.50',
                'step': '0.01',
                'min': '0',
                'max': '100',
            }),
            'special_achievement': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Any special achievements or awards (optional)',
            }),
        }
        labels = {
            'standard': 'Standard / Class',
            'medium': 'Medium of Instruction',
            'percentage_or_cgpa': 'Percentage / CGPA',
            'special_achievement': 'Special Achievement',
            'result_document': 'Result Document',
        }


class AdminRegistrationEditForm(forms.ModelForm):
    """Admin form for editing annual registrations."""

    class Meta:
        model = AnnualRegistration
        fields = [
            'standard', 'medium', 'percentage_or_cgpa',
            'special_achievement', 'result_document',
            'status', 'admin_remarks',
        ]
        widgets = {
            'standard': forms.TextInput(attrs={'class': 'form-control'}),
            'medium': forms.Select(attrs={'class': 'form-select'}),
            'percentage_or_cgpa': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
            }),
            'special_achievement': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
            }),
            'result_document': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.jpg,.jpeg,.png',
            }),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'admin_remarks': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Remarks for the applicant (visible if rejected)',
            }),
        }


class RegistrationFilterForm(forms.Form):
    """Filter form for admin registration list."""

    academic_year = forms.ChoiceField(
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    standard = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Standard',
        }),
    )
    medium = forms.ChoiceField(
        required=False,
        choices=[('', 'All Mediums')] + list(AnnualRegistration.Medium.choices),
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    status = forms.ChoiceField(
        required=False,
        choices=[('', 'All Statuses')] + list(AnnualRegistration.Status.choices),
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    village_city = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Village / City',
        }),
    )
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by Student ID, Name, Family ID...',
        }),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from apps.events.models import Event
        events = Event.objects.values_list('academic_year', 'academic_year').order_by('-academic_year')
        self.fields['academic_year'].choices = [('', 'All Years')] + list(events)
