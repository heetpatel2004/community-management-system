"""
Views for Student management — admin views.
"""

from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from apps.accounts.decorators import admin_required, registration_admin_required
from apps.families.models import Family

from .forms import StudentEditForm
from .models import Student


@admin_required
def admin_student_list(request):
    """Admin: List all students with search and filters."""
    search = request.GET.get('search', '').strip()
    status_filter = request.GET.get('status', '').strip()
    family_filter = request.GET.get('family_id', '').strip()

    students = Student.objects.select_related('family')

    if search:
        students = students.filter(
            Q(student_id__icontains=search) |
            Q(full_name__icontains=search) |
            Q(family__family_id__icontains=search) |
            Q(family__family_name__icontains=search) |
            Q(family__mobile_number__icontains=search)
        )

    if status_filter == 'active':
        students = students.filter(is_active=True)
    elif status_filter == 'inactive':
        students = students.filter(is_active=False)

    if family_filter:
        students = students.filter(family__family_id=family_filter)

    families = Family.objects.filter(is_active=True).order_by('family_id')

    paginator = Paginator(students, 25)
    page = request.GET.get('page')
    students_page = paginator.get_page(page)

    return render(request, 'students/admin_list.html', {
        'students': students_page,
        'search': search,
        'status_filter': status_filter,
        'family_filter': family_filter,
        'families': families,
        'total_count': students.count(),
    })


@admin_required
def admin_student_detail(request, pk):
    """Admin: View student profile with complete academic history."""
    student = get_object_or_404(
        Student.objects.select_related('family'),
        pk=pk,
    )
    registrations = (
        student.annual_registrations
        .select_related('event')
        .prefetch_related('awards__category')
        .order_by('-event__academic_year')
    )

    return render(request, 'students/admin_detail.html', {
        'student': student,
        'registrations': registrations,
    })


@registration_admin_required
def admin_student_edit(request, pk):
    """Admin: Edit student details."""
    student = get_object_or_404(Student, pk=pk)

    if request.method == 'POST':
        form = StudentEditForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, f'Student "{student.student_id}" updated successfully.')
            return redirect('students:admin_detail', pk=student.pk)
    else:
        form = StudentEditForm(instance=student)

    return render(request, 'students/admin_edit.html', {
        'form': form,
        'student': student,
    })
