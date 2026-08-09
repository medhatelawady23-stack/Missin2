from django.urls import path
from . import views

app_name = 'notes'

urlpatterns = [
    path('api/notes/', views.NotesAPIView.as_view(), name='api_notes'),
]
