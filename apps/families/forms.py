"""
Forms for Family registration and management.
"""

from django import forms
from .models import Family


class FamilyRegistrationForm(forms.ModelForm):
    """Public form for first-time family registration."""

    num_students = forms.IntegerField(
        min_value=1,
        max_value=20,
        initial=1,
        label='Number of Students',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '1',
            'max': '20',
        }),
        help_text='How many students do you want to register?',
    )

    class Meta:
        model = Family
        fields = ['family_name', 'responsible_person_name', 'mobile_number', 'village_city']
        widgets = {
            'family_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Patel Family / Patel & Sons',
            }),
            'responsible_person_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Rameshbhai Patel',
            }),
            'mobile_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 9876543210',
                'pattern': r'[0-9]{10,15}',
            }),
            'village_city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Kheralu',
            }),
        }
        labels = {
            'family_name': 'Family / Firm Name',
            'responsible_person_name': 'Responsible Person Name',
            'mobile_number': 'Mobile Number',
            'village_city': 'Village / City',
        }


class FamilyEditForm(forms.ModelForm):
    """Admin form for editing family details."""

    class Meta:
        model = Family
        fields = ['family_name', 'responsible_person_name', 'mobile_number', 'village_city', 'is_active']
        widgets = {
            'family_name': forms.TextInput(attrs={'class': 'form-control'}),
            'responsible_person_name': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile_number': forms.TextInput(attrs={'class': 'form-control'}),
            'village_city': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'family_name': 'Family / Firm Name',
            'responsible_person_name': 'Responsible Person Name',
            'mobile_number': 'Mobile Number',
            'village_city': 'Village / City',
            'is_active': 'Active',
        }


class FamilyLookupForm(forms.Form):
    """Public form to look up an existing family by Family ID."""

    family_id = forms.CharField(
        max_length=10,
        label='Family ID',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., FAM-00001',
            'autofocus': True,
        }),
        help_text='Enter your Family ID to access your family profile.',
    )

    def clean_family_id(self):
        family_id = self.cleaned_data['family_id'].strip().upper()
        if not family_id.startswith('FAM-'):
            raise forms.ValidationError('Family ID must start with "FAM-".')
        return family_id
