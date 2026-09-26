"""
Dashboard views — admin dashboard and error handlers.
"""

from django.db.models import Count, Q
from django.shortcuts import render, redirect

from apps.accounts.decorators import admin_required
from apps.families.models import Family
from apps.students.models import Student
from apps.events.models import Event
from apps.registrations.models import AnnualRegistration
from apps.awards.models import Award


def home(request):
    """Public homepage — redirect to lookup or dashboard."""
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('dashboard:admin_home')
    return render(request, 'dashboard/home.html')


@admin_required
def admin_dashboard(request):
    """Admin dashboard with key statistics."""
    # Get current open event
    current_event = Event.objects.filter(status=Event.Status.OPEN).first()

    # Overall statistics
    total_families = Family.objects.filter(is_active=True).count()
    total_students = Student.objects.filter(is_active=True).count()

    # Current event statistics
    current_registrations = 0
    pending_count = 0
    approved_count = 0
    rejected_count = 0
    under_review_count = 0

    if current_event:
        current_regs = AnnualRegistration.objects.filter(event=current_event)
        current_registrations = current_regs.count()
        pending_count = current_regs.filter(status=AnnualRegistration.Status.SUBMITTED).count()
        under_review_count = current_regs.filter(status=AnnualRegistration.Status.UNDER_REVIEW).count()
        approved_count = current_regs.filter(status=AnnualRegistration.Status.APPROVED).count()
        rejected_count = current_regs.filter(status=AnnualRegistration.Status.REJECTED).count()

    total_awards = Award.objects.count()

    # Recent registrations
    recent_registrations = (
        AnnualRegistration.objects
        .select_related('student__family', 'event')
        .order_by('-submitted_at')[:10]
    )

    # Registration by standard (for current event)
    standard_stats = []
    medium_stats = []
    if current_event:
        standard_stats = (
            AnnualRegistration.objects
            .filter(event=current_event)
            .values('standard')
            .annotate(count=Count('id'))
            .order_by('standard')
        )
        medium_stats = (
            AnnualRegistration.objects
            .filter(event=current_event)
            .values('medium')
            .annotate(count=Count('id'))
            .order_by('medium')
        )

    context = {
        'current_event': current_event,
        'total_families': total_families,
        'total_students': total_students,
        'current_registrations': current_registrations,
        'pending_count': pending_count,
        'under_review_count': under_review_count,
        'approved_count': approved_count,
        'rejected_count': rejected_count,
        'total_awards': total_awards,
        'recent_registrations': recent_registrations,
        'standard_stats': standard_stats,
        'medium_stats': medium_stats,
    }

    return render(request, 'dashboard/admin_dashboard.html', context)


@admin_required
def admin_search(request):
    """Global search across families, students, and registrations."""
    query = request.GET.get('q', '').strip()
    families = []
    students = []

    if query:
        families = Family.objects.filter(
            Q(family_id__icontains=query) |
            Q(family_name__icontains=query) |
            Q(responsible_person_name__icontains=query) |
            Q(mobile_number__icontains=query) |
            Q(village_city__icontains=query)
        )[:10]

        students = Student.objects.select_related('family').filter(
            Q(student_id__icontains=query) |
            Q(full_name__icontains=query) |
            Q(family__family_id__icontains=query)
        )[:10]

    return render(request, 'dashboard/search_results.html', {
        'query': query,
        'families': families,
        'students': students,
    })


# ──────────────────────────────────────────────
# ERROR HANDLERS
# ──────────────────────────────────────────────

def error_403(request, exception=None):
    return render(request, 'errors/403.html', status=403)


def error_404(request, exception=None):
    return render(request, 'errors/404.html', status=404)


def error_500(request):
    return render(request, 'errors/500.html', status=500)
