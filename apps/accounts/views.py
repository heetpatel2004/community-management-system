"""
Views for authentication and user management.
"""

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

from .decorators import super_admin_required
from .forms import LoginForm, AdminUserCreateForm, AdminUserUpdateForm
from .models import User


class AdminLoginView(LoginView):
    """Custom login view for admin panel."""
    template_name = 'accounts/login.html'
    form_class = LoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('dashboard:home')

    def form_valid(self, form):
        messages.success(self.request, f'Welcome back, {form.get_user().get_full_name() or form.get_user().username}!')
        return super().form_valid(form)


def admin_logout(request):
    """Log out the admin user."""
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('accounts:login')


@super_admin_required
def user_list(request):
    """List all admin users."""
    users = User.objects.filter(is_staff=True).order_by('username')
    return render(request, 'accounts/user_list.html', {'users': users})


@super_admin_required
def user_create(request):
    """Create a new admin user."""
    if request.method == 'POST':
        form = AdminUserCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True
            user.save()
            messages.success(request, f'User "{user.username}" created successfully.')
            return redirect('accounts:user_list')
    else:
        form = AdminUserCreateForm()

    return render(request, 'accounts/user_form.html', {
        'form': form,
        'title': 'Create Admin User',
        'button_text': 'Create User',
    })


@super_admin_required
def user_update(request, pk):
    """Update an admin user."""
    user = get_object_or_404(User, pk=pk, is_staff=True)

    if request.method == 'POST':
        form = AdminUserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f'User "{user.username}" updated successfully.')
            return redirect('accounts:user_list')
    else:
        form = AdminUserUpdateForm(instance=user)

    return render(request, 'accounts/user_form.html', {
        'form': form,
        'title': f'Edit User: {user.username}',
        'button_text': 'Update User',
        'editing': True,
    })


@super_admin_required
def user_toggle_active(request, pk):
    """Activate or deactivate an admin user."""
    user = get_object_or_404(User, pk=pk, is_staff=True)

    if user == request.user:
        messages.error(request, 'You cannot deactivate your own account.')
        return redirect('accounts:user_list')

    user.is_active = not user.is_active
    user.save(update_fields=['is_active'])

    status = 'activated' if user.is_active else 'deactivated'
    messages.success(request, f'User "{user.username}" has been {status}.')
    return redirect('accounts:user_list')
