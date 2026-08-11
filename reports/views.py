import json
from django.views import View
from django.views.generic import TemplateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from locations.models import Unit, LocationType, Location

from notes.models import Note, WorkType, WorkItemDetail, WorkActivity
from .models import Report, ReportItem, ReportItemImage


class ReportCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'reports/create.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['location_types'] = LocationType.objects.filter(is_active=True)
        work_types = WorkType.objects.filter(is_active=True)
        ctx['work_types'] = work_types
        ctx['work_types_json'] = json.dumps([{'id': wt.id, 'name': wt.name, 'category': getattr(wt, 'category', 'location')} for wt in work_types], ensure_ascii=False)
        
        work_elements = WorkItemDetail.objects.filter(is_active=True).select_related('work_type')
        ctx['work_elements_json'] = json.dumps([{'id': we.id, 'work_type_id': we.work_type_id, 'name': we.name} for we in work_elements], ensure_ascii=False)

        work_activities = WorkActivity.objects.filter(is_active=True).select_related('element')
        ctx['work_activities_json'] = json.dumps([{'id': wa.id, 'element_id': wa.element_id, 'name': wa.name} for wa in work_activities], ensure_ascii=False)

        ctx['units'] = Unit.objects.filter(is_active=True)

        # وحدة المستخدم ودور الحساب (مقاول / مراقب)
        user_unit = None
        role = 'contractor'
        if hasattr(self.request.user, 'profile'):
            if self.request.user.profile.unit:
                user_unit = self.request.user.profile.unit
            if self.request.user.profile.role:
                role = self.request.user.profile.role

        ctx['user_unit'] = user_unit
        ctx['user_role'] = role

        if role == 'supervisor':
            ctx['item_label_singular'] = 'ملاحظة'
            ctx['item_label_plural'] = 'ملاحظات'
            ctx['add_item_btn_text'] = 'إضافة ملاحظة'
            ctx['step4_title'] = 'العناصر التفصيلية والملاحظات الميدانية'
            ctx['step4_subtitle'] = 'أضف الملاحظات الميدانية حبة بحبة وصور كلاً منها بالكاميرا'
            ctx['empty_notes_title'] = 'لم تقم بإضافة أي ملاحظة بعد'
            ctx['empty_notes_subtitle'] = 'اضغط على زر (إضافة ملاحظة) بالأعلى للبدء في تسجيل الملاحظات والرصد'
        else:
            ctx['item_label_singular'] = 'نشاط'
            ctx['item_label_plural'] = 'أنشطة'
            ctx['add_item_btn_text'] = 'إضافة نشاط'
            ctx['step4_title'] = 'العناصر التفصيلية والأعمال الميدانية'
            ctx['step4_subtitle'] = 'أضف الأنشطة الميدانية حبة بحبة وصور كلاً منها بالكاميرا'
            ctx['empty_notes_title'] = 'لم تقم بإضافة أي نشاط بعد'
            ctx['empty_notes_subtitle'] = 'اضغط على زر (إضافة نشاط) بالأعلى للبدء في تسجيل الأعمال والأنشطة'

        return ctx


class ReportSubmitView(LoginRequiredMixin, View):
    def post(self, request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'بيانات غير صالحة'}, status=400)

        # التحقق من idempotency
        idempotency_key = data.get('idempotency_key')
        if idempotency_key:
            existing = Report.objects.filter(idempotency_key=idempotency_key).first()
            if existing:
                return JsonResponse({
                    'success': True,
                    'report_number': existing.report_number,
                    'report_id': existing.id,
                    'duplicate': True
                })

        location_type_id = data.get('location_type_id')
        location_id = data.get('location_id')
        unit_id = data.get('unit_id')
        selected_notes = data.get('notes', [])
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        location_photo_id = data.get('location_photo_id')

        # التحقق من GPS
        if not latitude or not longitude:
            return JsonResponse({'success': False, 'error': 'يرجى السماح بالوصول للموقع الجغرافي'}, status=400)

        # التحقق من صورة الموقع
        if not location_photo_id:
            return JsonResponse({'success': False, 'error': 'يرجى التقاط صورة تحديد الموقع'}, status=400)

        # التحقق من الحقول الأساسية
        if not all([location_type_id, location_id]):
            return JsonResponse({'success': False, 'error': 'يرجى اختيار نوع الموقع والموقع'}, status=400)

        if not selected_notes:
            return JsonResponse({'success': False, 'error': 'يرجى إضافة نشاط واحد على الأقل'}, status=400)

        # التحقق من عناصر التقرير وصورها
        for item_data in selected_notes:
            wt_id = item_data.get('work_type_id')
            if not wt_id:
                return JsonResponse({'success': False, 'error': 'يرجى اختيار نوع العمل لجميع الأنشطة المضافة'}, status=400)
            
            work_class = item_data.get('work_classification', '')
            work_detail_id = item_data.get('work_item_detail_id')
            if not work_class and not work_detail_id:
                return JsonResponse({'success': False, 'error': 'يرجى اختيار البند التفصيلي لجميع الأنشطة المضافة'}, status=400)

            image_ids = item_data.get('image_ids', [])
            if len(image_ids) < 2:
                return JsonResponse({'success': False, 'error': 'كل نشاط يجب أن يحتوي على صورتين على الأقل بالكاميرا'}, status=400)
            if len(image_ids) > 4:
                return JsonResponse({'success': False, 'error': 'كل نشاط لا يمكن أن يحتوي على أكثر من 4 صور'}, status=400)

        # الحصول على وحدة التقرير
        user_unit = None
        if hasattr(request.user, 'profile') and request.user.profile.unit:
            user_unit = request.user.profile.unit

        # إذا حدد الطلب وحدة مخصصة وكان الإداري يستطيع الاختبار أو لا توجد وحدة للمستخدم
        if unit_id and (request.user.is_staff or not user_unit):
            user_unit = Unit.objects.filter(id=unit_id).first()

        if not user_unit:
            return JsonResponse({'success': False, 'error': 'حسابك غير مرتبط بوحدة ولم تحدد وحدة. تواصل مع المسؤول.'}, status=400)

        location_type = get_object_or_404(LocationType, id=location_type_id)
        location = get_object_or_404(Location, id=location_id, unit=user_unit)


        # الحصول على صورة الموقع المؤقتة
        location_photo_obj = ReportItemImage.objects.filter(
            id=location_photo_id, report_item__isnull=True
        ).first()

        # إنشاء التقرير
        report = Report.objects.create(
            user=request.user,
            unit=user_unit,
            location_type=location_type,
            location=location,
            latitude=latitude,
            longitude=longitude,
            idempotency_key=idempotency_key or None,
        )

        # نقل صورة الموقع
        if location_photo_obj:
            report.location_photo = location_photo_obj.image
            report.save(update_fields=['location_photo'])
            location_photo_obj.delete()

        # إنشاء عناصر التقرير
        for item_data in selected_notes:
            work_type_id = item_data.get('work_type_id')
            work_item_detail_id = item_data.get('work_item_detail_id') or item_data.get('work_element_id')
            work_activity_id = item_data.get('work_activity_id')
            work_classification = item_data.get('work_classification', '')
            image_ids = item_data.get('image_ids', [])

            work_type = None
            if work_type_id:
                work_type = WorkType.objects.filter(id=work_type_id).first()

            work_item_detail = None
            if work_item_detail_id:
                work_item_detail = WorkItemDetail.objects.filter(id=work_item_detail_id).first()

            work_activity = None
            if work_activity_id:
                work_activity = WorkActivity.objects.filter(id=work_activity_id).first()
                if work_activity and not work_classification:
                    work_classification = work_activity.name
            elif work_item_detail and not work_classification:
                work_classification = work_item_detail.name

            report_item = ReportItem.objects.create(
                report=report,
                note=None,
                work_type=work_type,
                work_item_detail=work_item_detail,
                work_activity=work_activity,
                work_classification=work_classification,
            )

            # ربط الصور بعنصر التقرير
            ReportItemImage.objects.filter(
                id__in=image_ids,
                report_item__isnull=True
            ).update(report_item=report_item)


        return JsonResponse({
            'success': True,
            'report_number': report.report_number,
            'report_id': report.id,
        })


class ImageUploadView(LoginRequiredMixin, View):
    """رفع صورة مؤقتة (للملاحظات أو صورة الموقع)"""
    def post(self, request):
        image_file = request.FILES.get('image')
        if not image_file:
            return JsonResponse({'success': False, 'error': 'لا توجد صورة'}, status=400)

        img = ReportItemImage.objects.create(
            report_item_id=None,
            image=image_file
        )
        return JsonResponse({
            'success': True,
            'image_id': img.id,
            'image_url': img.image.url,
        })


class ReportDetailView(LoginRequiredMixin, DetailView):
    model = Report
    template_name = 'reports/detail.html'
    context_object_name = 'report'

    def get_queryset(self):
        """المستخدم يرى تقاريره فقط"""
        qs = super().get_queryset()
        if not self.request.user.is_staff:
            qs = qs.filter(user=self.request.user)
        return qs


class ReportSuccessView(LoginRequiredMixin, DetailView):
    model = Report
    template_name = 'reports/success.html'
    context_object_name = 'report'

    def get_queryset(self):
        """المستخدم يرى صفحة نجاح تقاريره فقط"""
        qs = super().get_queryset()
        if not self.request.user.is_staff:
            qs = qs.filter(user=self.request.user)
        return qs

