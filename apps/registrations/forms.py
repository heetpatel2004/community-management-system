"""
Forms for Annual Registration.
"""

from django import forms
from .models import AnnualRegistration
from .validators import validate_result_document


class AnnualRegistrationForm(forms.ModelForm):
    """Public form for yearly student registration."""

    SCHOOL_STANDARDS = [
        ('', 'Select Standard'),
        ('1', '1st'),
        ('2', '2nd'),
        ('3', '3rd'),
        ('4', '4th'),
        ('5', '5th'),
        ('6', '6th'),
        ('7', '7th'),
        ('8', '8th'),
        ('9', '9th'),
        ('10', '10th'),
        ('11 Sci-A', '11th Science (A)'),
        ('11 Sci-B', '11th Science (B)'),
        ('11 Commerce', '11th Commerce'),
        ('11 Arts', '11th Arts'),
        ('12 Sci-A', '12th Science (A)'),
        ('12 Sci-B', '12th Science (B)'),
        ('12 Commerce', '12th Commerce'),
        ('12 Arts', '12th Arts'),
    ]

    school_standard = forms.ChoiceField(
        choices=SCHOOL_STANDARDS,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Standard',
    )

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
        fields = ['institution_type', 'standard', 'medium', 'percentage_or_cgpa', 'special_achievement', 'result_document']
        widgets = {
            'institution_type': forms.Select(attrs={'class': 'form-select'}),
            'standard': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., B.Com Sem-1, B.Sc Sem-3',
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
            'institution_type': 'School or College',
            'standard': 'Standard / Course',
            'medium': 'Medium of Instruction',
            'percentage_or_cgpa': 'Percentage / CGPA',
            'special_achievement': 'Special Achievement',
            'result_document': 'Result Document',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make the model's standard field not required in the form;
        # we'll populate it in clean() from either school_standard or the text field.
        self.fields['standard'].required = False

    def clean(self):
        cleaned_data = super().clean()
        institution_type = cleaned_data.get('institution_type')
        school_standard = cleaned_data.get('school_standard')
        standard_text = cleaned_data.get('standard')

        if institution_type == 'school':
            if not school_standard:
                self.add_error('school_standard', 'Please select a standard.')
            else:
                cleaned_data['standard'] = school_standard
        elif institution_type == 'college':
            if not standard_text:
                self.add_error('standard', 'Please enter your course / semester.')
        else:
            self.add_error('institution_type', 'Please select School or College.')

        return cleaned_data


class AdminRegistrationEditForm(forms.ModelForm):
    """Admin form for editing annual registrations."""

    class Meta:
        model = AnnualRegistration
        fields = [
            'institution_type', 'standard', 'medium', 'percentage_or_cgpa',
            'special_achievement', 'result_document',
            'status', 'admin_remarks',
        ]
        widgets = {
            'institution_type': forms.Select(attrs={'class': 'form-select'}),
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

    STANDARD_CHOICES = [
        ('', 'All Standards'),
        ('1', '1st'),
        ('2', '2nd'),
        ('3', '3rd'),
        ('4', '4th'),
        ('5', '5th'),
        ('6', '6th'),
        ('7', '7th'),
        ('8', '8th'),
        ('9', '9th'),
        ('10', '10th'),
        ('11 Sci-A', '11th Science (A)'),
        ('11 Sci-B', '11th Science (B)'),
        ('11 Commerce', '11th Commerce'),
        ('11 Arts', '11th Arts'),
        ('12 Sci-A', '12th Science (A)'),
        ('12 Sci-B', '12th Science (B)'),
        ('12 Commerce', '12th Commerce'),
        ('12 Arts', '12th Arts'),
    ]

    academic_year = forms.ChoiceField(
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    institution_type = forms.ChoiceField(
        required=False,
        choices=[('', 'School & College')] + list(AnnualRegistration.InstitutionType.choices),
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    standard = forms.ChoiceField(
        required=False,
        choices=STANDARD_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
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

