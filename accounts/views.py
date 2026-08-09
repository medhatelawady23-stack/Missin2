from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages


class CustomLoginView(LoginView):
    """صفحة تسجيل دخول الموظفين الميدانيين"""
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('reports:create')


class AdminLoginView(LoginView):
    """صفحة تسجيل دخول مستقيلة خاصة بالإدارة"""
    template_name = 'accounts/admin_login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        user = form.get_user()
        if not user.is_staff:
            messages.error(self.request, 'عفواً، هذه الصفحة مخصصة لمدراء النظام والمشرفين فقط.')
            return self.form_invalid(form)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('dashboard:home')


class CustomLogoutView(LogoutView):
    """خروج الموظف الميداني إلى صفحة دخول الموظفين"""
    next_page = reverse_lazy('accounts:login')


class AdminLogoutView(LogoutView):
    """خروج المشرف والإداري إلى صفحة دخول الإدارة"""
    next_page = reverse_lazy('accounts:admin_login')

