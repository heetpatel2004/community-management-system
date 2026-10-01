"""
Family model — permanent family records with auto-generated Family ID.
"""

from django.db import models, transaction


class Family(models.Model):
    """
    Represents a permanent family record.
    Family ID (FAM-XXXXX) is auto-generated and never changes.
    A family can have multiple students.
    """

    family_id = models.CharField(
        max_length=10,
        unique=True,
        editable=False,
        db_index=True,
        help_text='Auto-generated permanent Family ID (e.g., FAM-00001)',
    )
    family_name = models.CharField(
        max_length=255,
        help_text='Family or firm name',
        db_index=True,
    )
    responsible_person_name = models.CharField(
        max_length=255,
        help_text='Name of the responsible person (head of family)',
    )
    mobile_number = models.CharField(
        max_length=15,
        db_index=True,
        help_text='Primary mobile number',
    )
    village_city = models.CharField(
        max_length=255,
        db_index=True,
        help_text='Village or city name',
    )
    is_active = models.BooleanField(
        default=True,
        help_text='Inactive families are hidden from public but data is preserved.',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Family'
        verbose_name_plural = 'Families'
        ordering = ['family_id']

    def __str__(self):
        return f"{self.family_id} — {self.family_name}"

    def save(self, *args, **kwargs):
        if not self.family_id:
            self.family_id = Family.generate_family_id()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_family_id():
        """
        Generate the next Family ID atomically.
        Format: FAM-XXXXX (e.g., FAM-00001)
        """
        with transaction.atomic():
            # Lock the table to prevent race conditions
            last = Family.objects.select_for_update().order_by('-id').first()
            next_num = (last.id if last else 0) + 1
            return f"FAM-{next_num:05d}"

    @property
    def student_count(self):
        return self.students.count()

    @property
    def active_student_count(self):
        return self.students.filter(is_active=True).count()
