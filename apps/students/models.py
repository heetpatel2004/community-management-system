"""
Student model — permanent student records with auto-generated Student ID.
"""

from django.db import models, transaction


class Student(models.Model):
    """
    Represents a permanent student record.
    Student ID (STU-XXXXX) is auto-generated and never changes.
    A student belongs to exactly one family.
    Annual academic details are stored separately in AnnualRegistration.
    """

    student_id = models.CharField(
        max_length=10,
        unique=True,
        editable=False,
        db_index=True,
        help_text='Auto-generated permanent Student ID (e.g., STU-00001)',
    )
    family = models.ForeignKey(
        'families.Family',
        on_delete=models.PROTECT,
        related_name='students',
        help_text='The family this student belongs to.',
    )
    full_name = models.CharField(
        max_length=255,
        db_index=True,
        help_text='Full name of the student',
    )
    is_active = models.BooleanField(
        default=True,
        help_text='Inactive students are hidden from public but data is preserved.',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'
        ordering = ['student_id']

    def __str__(self):
        return f"{self.student_id} — {self.full_name}"

    def save(self, *args, **kwargs):
        if not self.student_id:
            self.student_id = Student.generate_student_id()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_student_id():
        """
        Generate the next Student ID atomically.
        Format: STU-XXXXX (e.g., STU-00001)
        """
        with transaction.atomic():
            last = Student.objects.select_for_update().order_by('-id').first()
            next_num = (last.id if last else 0) + 1
            return f"STU-{next_num:05d}"
