"""
AnnualRegistration model — yearly academic records for students.
This is the core record linking a student to an event with academic details.
"""

import os
import uuid

from django.conf import settings
from django.db import models


def result_document_path(instance, filename):
    """Generate a secure, unique file path for uploaded result documents."""
    ext = os.path.splitext(filename)[1].lower()
    unique_name = f"{uuid.uuid4().hex}{ext}"
    year = instance.event.academic_year if instance.event else 'unknown'
    return f"result_documents/{year}/{unique_name}"


class AnnualRegistration(models.Model):
    """
    Yearly academic record for a student in a specific event.
    Each student can have at most ONE registration per event.
    Previous years' records are never overwritten.
    """

    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        SUBMITTED = 'submitted', 'Submitted'
        UNDER_REVIEW = 'under_review', 'Under Review'
        APPROVED = 'approved', 'Approved'
        REJECTED = 'rejected', 'Rejected'

    class Medium(models.TextChoices):
        GUJARATI = 'gujarati', 'Gujarati'
        ENGLISH = 'english', 'English'
        HINDI = 'hindi', 'Hindi'

    student = models.ForeignKey(
        'students.Student',
        on_delete=models.PROTECT,
        related_name='annual_registrations',
    )
    event = models.ForeignKey(
        'events.Event',
        on_delete=models.PROTECT,
        related_name='registrations',
    )
    standard = models.CharField(
        max_length=50,
        db_index=True,
        help_text='Standard/Class (e.g., 10, 11, 12, B.Com Sem-1)',
    )
    medium = models.CharField(
        max_length=20,
        choices=Medium.choices,
        db_index=True,
        help_text='Medium of instruction',
    )
    percentage_or_cgpa = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        help_text='Percentage or CGPA obtained',
    )
    special_achievement = models.TextField(
        blank=True,
        default='',
        help_text='Any special achievements or awards (optional)',
    )
    result_document = models.FileField(
        upload_to=result_document_path,
        blank=True,
        null=True,
        help_text='Upload result document (PDF, JPG, PNG — max 5MB)',
    )
    status = models.CharField(
        max_length=15,
        choices=Status.choices,
        default=Status.SUBMITTED,
        db_index=True,
    )
    admin_remarks = models.TextField(
        blank=True,
        default='',
        help_text='Remarks by admin during verification',
    )
    submitted_at = models.DateTimeField(auto_now_add=True)
    verified_at = models.DateTimeField(null=True, blank=True)
    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='verified_registrations',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Annual Registration'
        verbose_name_plural = 'Annual Registrations'
        ordering = ['-event__academic_year', 'student__student_id']
        # Prevent duplicate registrations: one student per event
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'event'],
                name='unique_student_event_registration',
            )
        ]
        indexes = [
            models.Index(fields=['student', 'event']),
            models.Index(fields=['event', 'status']),
            models.Index(fields=['event', 'standard']),
            models.Index(fields=['event', 'medium']),
        ]

    def __str__(self):
        return f"{self.student.student_id} — {self.event.academic_year} — {self.standard}"

    @property
    def family(self):
        return self.student.family
