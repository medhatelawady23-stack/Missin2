from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('create/', views.ReportCreateView.as_view(), name='create'),
    path('submit/', views.ReportSubmitView.as_view(), name='submit'),
    path('upload-image/', views.ImageUploadView.as_view(), name='upload_image'),
    path('<int:pk>/', views.ReportDetailView.as_view(), name='detail'),
    path('<int:pk>/success/', views.ReportSuccessView.as_view(), name='success'),
]
