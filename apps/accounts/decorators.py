"""
Custom decorators for role-based access control.
"""

from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def admin_required(view_func):
    """Require any admin role to access the view."""
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff and not request.user.is_superuser:
            raise PermissionDenied("You do not have permission to access this page.")
        return view_func(request, *args, **kwargs)
    return wrapper


def super_admin_required(view_func):
    """Require super admin role."""
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if not request.user.is_super_admin:
            raise PermissionDenied("Only Super Admins can access this page.")
        return view_func(request, *args, **kwargs)
    return wrapper


def registration_admin_required(view_func):
    """Require registration admin or super admin role."""
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if not request.user.is_registration_admin:
            raise PermissionDenied("You do not have permission to manage registrations.")
        return view_func(request, *args, **kwargs)
    return wrapper


def verification_admin_required(view_func):
    """Require verification admin or super admin role."""
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if not request.user.is_verification_admin:
            raise PermissionDenied("You do not have permission to verify registrations.")
        return view_func(request, *args, **kwargs)
    return wrapper


def report_staff_required(view_func):
    """Require any admin role (all admins can access reports)."""
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if not request.user.is_report_staff:
            raise PermissionDenied("You do not have permission to access reports.")
        return view_func(request, *args, **kwargs)
    return wrapper
