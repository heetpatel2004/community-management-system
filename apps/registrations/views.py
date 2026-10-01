"""
Views for Annual Registration — public submission and admin management.
"""

from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from apps.accounts.decorators import admin_required, verification_admin_required
from apps.events.models import Event
from apps.families.models import Family
from apps.students.models import Student

from .forms import AnnualRegistrationForm, AdminRegistrationEditForm, RegistrationFilterForm
from .models import AnnualRegistration


# ──────────────────────────────────────────────
# PUBLIC VIEWS
# ──────────────────────────────────────────────

def public_register(request, family_id, student_pk):
    """Public: Submit annual registration for a student."""
    family = get_object_or_404(Family, family_id=family_id, is_active=True)
    student = get_object_or_404(Student, pk=student_pk, family=family, is_active=True)

    # Get open events
    open_events = Event.objects.filter(status=Event.Status.OPEN)
    if not open_events.exists():
        messages.warning(request, 'No events are currently open for registration.')
        return redirect('families:lookup')

    if request.method == 'POST':
        form = AnnualRegistrationForm(request.POST, request.FILES)
        event_id = request.POST.get('event')

        if form.is_valid() and event_id:
            event = get_object_or_404(Event, pk=event_id, status=Event.Status.OPEN)

            # Check for duplicate
            if AnnualRegistration.objects.filter(student=student, event=event).exists():
                messages.error(
                    request,
                    f'{student.full_name} is already registered for {event.academic_year}. '
                    f'Duplicate registrations are not allowed.'
                )
                return render(request, 'registrations/public_form.html', {
                    'form': form,
                    'family': family,
                    'student': student,
                    'open_events': open_events,
                })

            registration = form.save(commit=False)
            registration.student = student
            registration.event = event
            registration.status = AnnualRegistration.Status.SUBMITTED
            registration.save()

            return render(request, 'registrations/public_success.html', {
                'registration': registration,
                'family': family,
                'student': student,
            })
        else:
            if not event_id:
                messages.error(request, 'Please select an event.')
    else:
        form = AnnualRegistrationForm()

    return render(request, 'registrations/public_form.html', {
        'form': form,
        'family': family,
        'student': student,
        'open_events': open_events,
    })


# ──────────────────────────────────────────────
# ADMIN VIEWS
# ──────────────────────────────────────────────

def public_edit_registration(request, family_id, pk):
    """Public: Edit a submitted/draft registration from the family portal."""
    family = get_object_or_404(Family, family_id=family_id, is_active=True)
    registration = get_object_or_404(
        AnnualRegistration.objects.select_related('student__family', 'event'),
        pk=pk,
        student__family=family,
    )

    # Only allow editing draft or submitted registrations
    if registration.status not in [AnnualRegistration.Status.DRAFT, AnnualRegistration.Status.SUBMITTED]:
        messages.error(request, 'This registration has already been reviewed and cannot be edited.')
        return redirect('families:edit_student', family_id=family.family_id, student_pk=registration.student.pk)

    if request.method == 'POST':
        form = AnnualRegistrationForm(request.POST, request.FILES, instance=registration)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration updated successfully.')
            return redirect('families:edit_student', family_id=family.family_id, student_pk=registration.student.pk)
    else:
        # Pre-populate school_standard if institution_type is school
        initial = {}
        if registration.institution_type == 'school':
            initial['school_standard'] = registration.standard
        form = AnnualRegistrationForm(instance=registration, initial=initial)

    return render(request, 'registrations/public_edit.html', {
        'form': form,
        'family': family,
        'student': registration.student,
        'registration': registration,
    })


# ──────────────────────────────────────────────
# ADMIN VIEWS (continued)
# ──────────────────────────────────────────────

@admin_required
def admin_registration_list(request):
    """Admin: List all registrations with filters."""
    filter_form = RegistrationFilterForm(request.GET)

    registrations = (
        AnnualRegistration.objects
        .select_related('student__family', 'event', 'verified_by')
        .prefetch_related('awards__category')
    )

    # Apply filters
    if filter_form.is_valid():
        data = filter_form.cleaned_data

        if data.get('academic_year'):
            registrations = registrations.filter(event__academic_year=data['academic_year'])
        if data.get('institution_type'):
            registrations = registrations.filter(institution_type=data['institution_type'])
        if data.get('standard'):
            registrations = registrations.filter(standard=data['standard'])
        if data.get('medium'):
            registrations = registrations.filter(medium=data['medium'])
        if data.get('status'):
            registrations = registrations.filter(status=data['status'])
        if data.get('village_city'):
            registrations = registrations.filter(student__family__village_city__icontains=data['village_city'])
        if data.get('search'):
            search = data['search']
            registrations = registrations.filter(
                Q(student__student_id__icontains=search) |
                Q(student__full_name__icontains=search) |
                Q(student__family__family_id__icontains=search) |
                Q(student__family__family_name__icontains=search)
            )

    registrations = registrations.order_by('-submitted_at')

    paginator = Paginator(registrations, 25)
    page = request.GET.get('page')
    registrations_page = paginator.get_page(page)

    return render(request, 'registrations/admin_list.html', {
        'registrations': registrations_page,
        'filter_form': filter_form,
        'total_count': registrations.count(),
    })


@admin_required
def admin_registration_detail(request, pk):
    """Admin: View registration details."""
    registration = get_object_or_404(
        AnnualRegistration.objects
        .select_related('student__family', 'event', 'verified_by')
        .prefetch_related('awards__category'),
        pk=pk,
    )

    return render(request, 'registrations/admin_detail.html', {
        'registration': registration,
    })


@verification_admin_required
def admin_registration_edit(request, pk):
    """Admin: Edit a registration."""
    registration = get_object_or_404(
        AnnualRegistration.objects.select_related('student__family', 'event'),
        pk=pk,
    )

    if request.method == 'POST':
        form = AdminRegistrationEditForm(request.POST, request.FILES, instance=registration)
        if form.is_valid():
            reg = form.save(commit=False)
            # If status changed to approved/rejected, update verification fields
            if reg.status in [AnnualRegistration.Status.APPROVED, AnnualRegistration.Status.REJECTED]:
                reg.verified_at = timezone.now()
                reg.verified_by = request.user
            reg.save()
            messages.success(request, 'Registration updated successfully.')
            return redirect('registrations:admin_detail', pk=registration.pk)
    else:
        form = AdminRegistrationEditForm(instance=registration)

    return render(request, 'registrations/admin_edit.html', {
        'form': form,
        'registration': registration,
    })


@verification_admin_required
def admin_registration_verify(request, pk, action):
    """Admin: Quick approve or reject a registration."""
    registration = get_object_or_404(AnnualRegistration, pk=pk)

    if action == 'approve':
        registration.status = AnnualRegistration.Status.APPROVED
        registration.verified_at = timezone.now()
        registration.verified_by = request.user
        registration.save()
        messages.success(request, f'Registration for {registration.student.student_id} approved.')
    elif action == 'reject':
        remarks = request.POST.get('admin_remarks', '')
        registration.status = AnnualRegistration.Status.REJECTED
        registration.admin_remarks = remarks
        registration.verified_at = timezone.now()
        registration.verified_by = request.user
        registration.save()
        messages.success(request, f'Registration for {registration.student.student_id} rejected.')
    else:
        messages.error(request, 'Invalid action.')

    return redirect(request.META.get('HTTP_REFERER', 'registrations:admin_list'))
