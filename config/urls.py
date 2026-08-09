"""URL configuration for FieldReport project."""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('admin/', include('reports.dashboard_urls', namespace='dashboard')),
    path('dashboard/', RedirectView.as_view(url='/admin/', permanent=False)),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('locations/', include('locations.urls', namespace='locations')),
    path('notes/', include('notes.urls', namespace='notes')),
    path('reports/', include('reports.urls', namespace='reports')),
    path('', RedirectView.as_view(url='/reports/create/', permanent=False)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
