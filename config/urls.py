"""
URL configuration for Saraswati Sanman Samaroh.
"""

from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    # Django admin (kept as fallback)
    path('django-admin/', admin.site.urls),

    # Project apps
    path('', include('apps.dashboard.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('families/', include('apps.families.urls')),
    path('students/', include('apps.students.urls')),
    path('events/', include('apps.events.urls')),
    path('registrations/', include('apps.registrations.urls')),
    path('awards/', include('apps.awards.urls')),
    path('reports/', include('apps.reports.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Custom error handlers
handler403 = 'apps.dashboard.views.error_403'
handler404 = 'apps.dashboard.views.error_404'
handler500 = 'apps.dashboard.views.error_500'
