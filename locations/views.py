from django.views import View
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Location
from notes.models import WorkType


class LocationsAPIView(LoginRequiredMixin, View):
    """API: جلب المواقع — مفلترة بالوحدة ونوع الموقع"""
    def get(self, request):
        type_id = request.GET.get('type') or request.GET.get('type_id')
        unit_id = request.GET.get('unit') or request.GET.get('unit_id')

        # الحصول على وحدة المستخدم
        user_unit = None
        if hasattr(request.user, 'profile') and request.user.profile.unit:
            user_unit = request.user.profile.unit

        qs = Location.objects.filter(is_active=True).select_related('unit', 'location_type')

        # إذا حدد الطلب وحدة مخصصة نستخدمها، وإلا إذا كان مستخدماً عادياً نستخدم وحدته
        if unit_id:
            qs = qs.filter(unit_id=unit_id)
        elif user_unit and not request.user.is_staff:
            qs = qs.filter(unit=user_unit)

        if type_id:
            qs = qs.filter(location_type_id=type_id)

        data = [
            {
                'id': loc.id,
                'name': loc.name,
                'unit_id': loc.unit_id,
                'unit_name': loc.unit.name,
                'type_id': loc.location_type_id,
                'type_name': loc.location_type.name,
            }
            for loc in qs
        ]
        return JsonResponse({'locations': data})



class WorkTypesAPIView(LoginRequiredMixin, View):
    """API: جلب أنواع العمل"""
    def get(self, request):
        work_types = WorkType.objects.filter(is_active=True)
        data = [{'id': wt.id, 'name': wt.name} for wt in work_types]
        return JsonResponse({'work_types': data})
