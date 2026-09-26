"""
Views for Reports — filter-based reporting with export support.
"""

from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render

from apps.accounts.decorators import admin_required
from apps.events.models import Event
from apps.registrations.models import AnnualRegistration
from apps.registrations.forms import RegistrationFilterForm

from .exporters import export_csv, export_excel, export_pdf


@admin_required
def report_view(request):
    """Admin: Generate filtered reports with export."""
    filter_form = RegistrationFilterForm(request.GET)

    registrations = (
        AnnualRegistration.objects
        .select_related('student__family', 'event', 'verified_by')
        .prefetch_related('awards__category')
    )

    # Apply filters
    active_filters = {}
    if filter_form.is_valid():
        data = filter_form.cleaned_data

        if data.get('academic_year'):
            registrations = registrations.filter(event__academic_year=data['academic_year'])
            active_filters['Academic Year'] = data['academic_year']
        if data.get('standard'):
            registrations = registrations.filter(standard__icontains=data['standard'])
            active_filters['Standard'] = data['standard']
        if data.get('medium'):
            registrations = registrations.filter(medium=data['medium'])
            active_filters['Medium'] = dict(AnnualRegistration.Medium.choices).get(data['medium'], data['medium'])
        if data.get('status'):
            registrations = registrations.filter(status=data['status'])
            active_filters['Status'] = dict(AnnualRegistration.Status.choices).get(data['status'], data['status'])
        if data.get('village_city'):
            registrations = registrations.filter(student__family__village_city__icontains=data['village_city'])
            active_filters['Village/City'] = data['village_city']
        if data.get('search'):
            search = data['search']
            registrations = registrations.filter(
                Q(student__student_id__icontains=search) |
                Q(student__full_name__icontains=search) |
                Q(student__family__family_id__icontains=search) |
                Q(student__family__family_name__icontains=search)
            )
            active_filters['Search'] = search

    registrations = registrations.order_by('student__student_id')

    # Handle export
    export_format = request.GET.get('export')
    if export_format == 'csv':
        return export_csv(registrations)
    elif export_format == 'excel':
        return export_excel(registrations)
    elif export_format == 'pdf':
        title_parts = ['Saraswati Sanman Samaroh Report']
        if active_filters:
            title_parts.append(' — '.join(f'{k}: {v}' for k, v in active_filters.items()))
        return export_pdf(registrations, title=' | '.join(title_parts))

    # Pagination for display
    total_count = registrations.count()
    paginator = Paginator(registrations, 50)
    page = request.GET.get('page')
    registrations_page = paginator.get_page(page)

    return render(request, 'reports/report.html', {
        'registrations': registrations_page,
        'filter_form': filter_form,
        'total_count': total_count,
        'active_filters': active_filters,
    })
