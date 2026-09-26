"""
Award models — categories and individual award records.
"""

from django.db import models


class AwardCategory(models.Model):
    """
    Award category that can be assigned to students.
    Admin can add/edit/deactivate categories.
    """

    name = models.CharField(
        max_length=255,
        unique=True,
        help_text='Name of the award category (e.g., Academic Excellence)',
    )
    description = models.TextField(
        blank=True,
        default='',
        help_text='Description of the award category',
    )
    is_active = models.BooleanField(
        default=True,
        help_text='Inactive categories are hidden but preserved.',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Award Category'
        verbose_name_plural = 'Award Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Award(models.Model):
    """
    Individual award given to a student's annual registration.
    A student can receive different awards in different years.
    """

    annual_registration = models.ForeignKey(
        'registrations.AnnualRegistration',
        on_delete=models.PROTECT,
        related_name='awards',
        help_text='The annual registration this award is for.',
    )
    category = models.ForeignKey(
        AwardCategory,
        on_delete=models.PROTECT,
        related_name='awards',
    )
    remarks = models.TextField(
        blank=True,
        default='',
        help_text='Additional remarks about this award',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Award'
        verbose_name_plural = 'Awards'
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['annual_registration', 'category'],
                name='unique_award_per_registration_category',
            )
        ]

    def __str__(self):
        return f"{self.annual_registration.student.student_id} — {self.category.name} ({self.annual_registration.event.academic_year})"
