"""
Custom User model with role-based access control.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model with role support for admin staff."""

    class Role(models.TextChoices):
        SUPER_ADMIN = 'super_admin', 'Super Admin'
        REGISTRATION_ADMIN = 'registration_admin', 'Registration Admin'
        VERIFICATION_ADMIN = 'verification_admin', 'Verification Admin'
        REPORT_STAFF = 'report_staff', 'Report Staff'

    role = models.CharField(
        max_length=30,
        choices=Role.choices,
        default=Role.REGISTRATION_ADMIN,
        help_text='Determines the permissions this user has in the admin panel.',
    )

    class Meta:
        ordering = ['username']

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"

    @property
    def is_super_admin(self):
        return self.role == self.Role.SUPER_ADMIN or self.is_superuser

    @property
    def is_registration_admin(self):
        return self.role in [self.Role.SUPER_ADMIN, self.Role.REGISTRATION_ADMIN] or self.is_superuser

    @property
    def is_verification_admin(self):
        return self.role in [self.Role.SUPER_ADMIN, self.Role.VERIFICATION_ADMIN] or self.is_superuser

    @property
    def is_report_staff(self):
        return self.role in [
            self.Role.SUPER_ADMIN,
            self.Role.REGISTRATION_ADMIN,
            self.Role.VERIFICATION_ADMIN,
            self.Role.REPORT_STAFF,
        ] or self.is_superuser
