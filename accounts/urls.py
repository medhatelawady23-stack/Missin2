from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('admin/login/', views.AdminLoginView.as_view(), name='admin_login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('admin/logout/', views.AdminLogoutView.as_view(), name='admin_logout'),
]

