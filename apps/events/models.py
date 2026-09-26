"""
Event model — annual Saraswati Sanman Samaroh events.
"""

from django.db import models


class Event(models.Model):
    """
    Represents a yearly Saraswati Sanman Samaroh event.
    Each academic year has exactly one event record.
    """

    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        OPEN = 'open', 'Open for Registration'
        CLOSED = 'closed', 'Closed'

    event_name = models.CharField(
        max_length=500,
        default='Shree Akhil Bharatiya Kutch Kadva Patidar Sanatan Samaj Kheralu Ayojit Saraswati Sanman Samaroh',
        help_text='Full name of the event',
    )
    academic_year = models.CharField(
        max_length=10,
        unique=True,
        db_index=True,
        help_text='Academic year (e.g., 2026-27)',
    )
    event_date = models.DateField(
        null=True,
        blank=True,
        help_text='Date when the ceremony will be held',
    )
    registration_start_date = models.DateField(
        null=True,
        blank=True,
        help_text='When registrations open',
    )
    registration_end_date = models.DateField(
        null=True,
        blank=True,
        help_text='When registrations close',
    )
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.DRAFT,
        db_index=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
        ordering = ['-academic_year']

    def __str__(self):
        return f"Saraswati Sanman Samaroh — {self.academic_year}"

    @property
    def is_open(self):
        return self.status == self.Status.OPEN

    @property
    def is_closed(self):
        return self.status == self.Status.CLOSED

    @property
    def display_name(self):
        return f"Saraswati Sanman Samaroh — {self.academic_year}"
