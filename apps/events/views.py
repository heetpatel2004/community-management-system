"""
Views for Event management — admin only.
"""

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from apps.accounts.decorators import admin_required, super_admin_required

from .forms import EventForm
from .models import Event


@admin_required
def admin_event_list(request):
    """Admin: List all events."""
    events = Event.objects.all()
    return render(request, 'events/admin_list.html', {'events': events})


@super_admin_required
def admin_event_create(request):
    """Admin: Create a new event."""
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event created successfully.')
            return redirect('events:admin_list')
    else:
        form = EventForm()

    return render(request, 'events/admin_form.html', {
        'form': form,
        'title': 'Create New Event',
        'button_text': 'Create Event',
    })


@super_admin_required
def admin_event_edit(request, pk):
    """Admin: Edit an event."""
    event = get_object_or_404(Event, pk=pk)

    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, f'Event "{event.academic_year}" updated successfully.')
            return redirect('events:admin_list')
    else:
        form = EventForm(instance=event)

    return render(request, 'events/admin_form.html', {
        'form': form,
        'title': f'Edit Event: {event.academic_year}',
        'button_text': 'Update Event',
        'event': event,
    })


@super_admin_required
def admin_event_change_status(request, pk, new_status):
    """Admin: Change event status (draft/open/closed)."""
    event = get_object_or_404(Event, pk=pk)

    valid_statuses = dict(Event.Status.choices)
    if new_status not in valid_statuses:
        messages.error(request, 'Invalid status.')
        return redirect('events:admin_list')

    old_status = event.get_status_display()
    event.status = new_status
    event.save(update_fields=['status', 'updated_at'])

    messages.success(request, f'Event "{event.academic_year}" status changed from "{old_status}" to "{event.get_status_display()}".')
    return redirect('events:admin_list')
