"""
Views for Award management — admin only.
"""

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from apps.accounts.decorators import admin_required, super_admin_required
from apps.registrations.models import AnnualRegistration

from .forms import AwardCategoryForm, AwardForm
from .models import AwardCategory, Award


@admin_required
def admin_category_list(request):
    """Admin: List all award categories."""
    categories = AwardCategory.objects.all()
    return render(request, 'awards/admin_category_list.html', {'categories': categories})


@super_admin_required
def admin_category_create(request):
    """Admin: Create award category."""
    if request.method == 'POST':
        form = AwardCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Award category created successfully.')
            return redirect('awards:admin_category_list')
    else:
        form = AwardCategoryForm()

    return render(request, 'awards/admin_category_form.html', {
        'form': form,
        'title': 'Create Award Category',
        'button_text': 'Create Category',
    })


@super_admin_required
def admin_category_edit(request, pk):
    """Admin: Edit award category."""
    category = get_object_or_404(AwardCategory, pk=pk)

    if request.method == 'POST':
        form = AwardCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, f'Award category "{category.name}" updated.')
            return redirect('awards:admin_category_list')
    else:
        form = AwardCategoryForm(instance=category)

    return render(request, 'awards/admin_category_form.html', {
        'form': form,
        'title': f'Edit Category: {category.name}',
        'button_text': 'Update Category',
    })


@admin_required
def admin_award_list(request):
    """Admin: List all awards."""
    awards = (
        Award.objects
        .select_related('annual_registration__student__family', 'annual_registration__event', 'category')
        .order_by('-created_at')
    )

    # Filter by event
    event_year = request.GET.get('event', '')
    if event_year:
        awards = awards.filter(annual_registration__event__academic_year=event_year)

    from apps.events.models import Event
    events = Event.objects.values_list('academic_year', 'academic_year').order_by('-academic_year')

    return render(request, 'awards/admin_list.html', {
        'awards': awards,
        'events': events,
        'selected_event': event_year,
    })


@super_admin_required
def admin_award_create(request, registration_pk):
    """Admin: Assign an award to a registration."""
    registration = get_object_or_404(
        AnnualRegistration.objects.select_related('student', 'event'),
        pk=registration_pk,
    )

    if request.method == 'POST':
        form = AwardForm(request.POST)
        if form.is_valid():
            award = form.save(commit=False)
            award.annual_registration = registration

            # Check for duplicate
            if Award.objects.filter(
                annual_registration=registration,
                category=award.category,
            ).exists():
                messages.error(request, 'This student already has this award for this event.')
            else:
                award.save()
                messages.success(request, f'Award "{award.category.name}" assigned to {registration.student.student_id}.')
                return redirect('registrations:admin_detail', pk=registration.pk)
    else:
        form = AwardForm()

    return render(request, 'awards/admin_award_form.html', {
        'form': form,
        'registration': registration,
    })


@super_admin_required
def admin_award_delete(request, pk):
    """Admin: Remove an award."""
    award = get_object_or_404(Award.objects.select_related('annual_registration'), pk=pk)
    registration_pk = award.annual_registration.pk
    award.delete()
    messages.success(request, 'Award removed successfully.')
    return redirect('registrations:admin_detail', pk=registration_pk)
