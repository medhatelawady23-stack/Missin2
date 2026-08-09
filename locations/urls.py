from django.urls import path
from . import views

app_name = 'locations'

urlpatterns = [
    path('api/locations/', views.LocationsAPIView.as_view(), name='api_locations'),
    path('api/work-types/', views.WorkTypesAPIView.as_view(), name='api_work_types'),
]
