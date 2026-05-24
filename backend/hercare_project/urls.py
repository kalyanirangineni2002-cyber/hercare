"""
URL configuration for hercare_project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('accounts/', include('accounts.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('cycle-tracker/', include('cycle_tracker.urls')),
    path('appointments/', include('appointments.urls')),
    path('mental-health/', include('mental_health.urls')),
    path('nutrition/', include('nutrition.urls')),
    path('reminders/', include('reminders.urls')),
    path('health-reports/', include('health_reports.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
