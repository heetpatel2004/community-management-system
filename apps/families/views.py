"""
Views for Family management — both public and admin.
"""

from django.contrib import messages
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q, Count
from django.shortcuts import render, redirect, get_object_or_404

from apps.accounts.decorators import admin_required, registration_admin_required
from apps.students.models import Student

from .forms import FamilyRegistrationForm, FamilyEditForm, FamilyLookupForm
from .models import Family


# ──────────────────────────────────────────────
# PUBLIC VIEWS
# ──────────────────────────────────────────────

def family_register(request):
    """Public: First-time family registration with students."""
    from apps.events.models import Event
    open_events = Event.objects.filter(status=Event.Status.OPEN)

    if request.method == 'POST':
        form = FamilyRegistrationForm(request.POST)
        student_names = request.POST.getlist('student_name')

        if form.is_valid() and student_names:
            with transaction.atomic():
                family = form.save()

                created_students = []
                for name in student_names:
                    name = name.strip()
                    if name:
                        student = Student(family=family, full_name=name)
                        student.save()
                        created_students.append(student)

                if not created_students:
                    messages.error(request, 'Please enter at least one student name.')
                    return render(request, 'families/register.html', {
                        'form': form,
                        'has_open_events': open_events.exists(),
                    })

            return render(request, 'families/registration_success.html', {
                'family': family,
                'students': created_students,
            })
        else:
            if not student_names:
                messages.error(request, 'Please enter at least one student name.')
    else:
        form = FamilyRegistrationForm()

    return render(request, 'families/register.html', {
        'form': form,
        'has_open_events': open_events.exists(),
    })


def family_lookup(request):
    """Public: Look up an existing family by Family ID."""
    form = FamilyLookupForm()
    family = None
    error = None

    if request.method == 'POST':
        form = FamilyLookupForm(request.POST)
        if form.is_valid():
            family_id = form.cleaned_data['family_id']
            try:
                family = Family.objects.get(family_id=family_id, is_active=True)
                students = family.students.filter(is_active=True)
                return render(request, 'families/family_portal.html', {
                    'family': family,
                    'students': students,
                })
            except Family.DoesNotExist:
                error = f'No active family found with ID "{family_id}". Please check the ID and try again.'

    return render(request, 'families/lookup.html', {
        'form': form,
        'error': error,
    })


def family_add_student(request, family_id):
    """Public: Add a new student to an existing family."""
    family = get_object_or_404(Family, family_id=family_id, is_active=True)

    if request.method == 'POST':
        name = request.POST.get('full_name', '').strip()
        if name:
            with transaction.atomic():
                student = Student(family=family, full_name=name)
                student.save()
            messages.success(request, f'Student "{student.full_name}" added successfully. Student ID: {student.student_id}')
        else:
            messages.error(request, 'Please enter the student name.')

    students = family.students.filter(is_active=True)
    return render(request, 'families/family_portal.html', {
        'family': family,
        'students': students,
    })


# ──────────────────────────────────────────────
# ADMIN VIEWS
# ──────────────────────────────────────────────

@admin_required
def admin_family_list(request):
    """Admin: List all families with search and filter."""
    search = request.GET.get('search', '').strip()
    families = Family.objects.annotate(student_count_val=Count('students'))

    if search:
        families = families.filter(
            Q(family_id__icontains=search) |
            Q(family_name__icontains=search) |
            Q(responsible_person_name__icontains=search) |
            Q(mobile_number__icontains=search) |
            Q(village_city__icontains=search)
        )

    paginator = Paginator(families, 25)
    page = request.GET.get('page')
    families_page = paginator.get_page(page)

    return render(request, 'families/admin_list.html', {
        'families': families_page,
        'search': search,
        'total_count': families.count(),
    })


@admin_required
def admin_family_detail(request, pk):
    """Admin: View family details with all students and history."""
    family = get_object_or_404(Family, pk=pk)
    students = family.students.all().prefetch_related('annual_registrations__event', 'annual_registrations__awards__category')

    return render(request, 'families/admin_detail.html', {
        'family': family,
        'students': students,
    })


@registration_admin_required
def admin_family_edit(request, pk):
    """Admin: Edit family details."""
    family = get_object_or_404(Family, pk=pk)

    if request.method == 'POST':
        form = FamilyEditForm(request.POST, instance=family)
        if form.is_valid():
            form.save()
            messages.success(request, f'Family "{family.family_id}" updated successfully.')
            return redirect('families:admin_detail', pk=family.pk)
    else:
        form = FamilyEditForm(instance=family)

    return render(request, 'families/admin_edit.html', {
        'form': form,
        'family': family,
    })


@registration_admin_required
def admin_family_add_student(request, pk):
    """Admin: Add a student to a family."""
    family = get_object_or_404(Family, pk=pk)

    if request.method == 'POST':
        name = request.POST.get('full_name', '').strip()
        if name:
            with transaction.atomic():
                student = Student(family=family, full_name=name)
                student.save()
            messages.success(request, f'Student "{student.full_name}" ({student.student_id}) added to family {family.family_id}.')
        else:
            messages.error(request, 'Please enter the student name.')

    return redirect('families:admin_detail', pk=family.pk)
