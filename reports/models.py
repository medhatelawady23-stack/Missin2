from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from locations.models import Unit, LocationType, Location


def generate_report_number():
    """توليد رقم تقرير تلقائي: RPT-YYYYMMDD-XXXX"""
    today = timezone.localdate()
    date_str = today.strftime('%Y%m%d')
    prefix = f'RPT-{date_str}-'
    last = Report.objects.filter(report_number__startswith=prefix).order_by('report_number').last()
    if last:
        last_seq = int(last.report_number.split('-')[-1])
        new_seq = last_seq + 1
    else:
        new_seq = 1
    return f'{prefix}{new_seq:04d}'


def location_photo_path(instance, filename):
    """مسار حفظ صورة تحديد الموقع"""
    return f'reports/location_photos/{filename}'


class Report(models.Model):
    """التقرير الميداني الرئيسي"""
    report_number = models.CharField(
        max_length=30, unique=True, editable=False,
        verbose_name='رقم التقرير'
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='reports', verbose_name='المستخدم'
    )
    unit = models.ForeignKey(
        Unit, on_delete=models.CASCADE,
        related_name='reports', verbose_name='وحدة التنسيق'
    )
    location_type = models.ForeignKey(
        LocationType, on_delete=models.CASCADE,
        related_name='reports', verbose_name='تصنيف الموقع'
    )
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE,
        related_name='reports', verbose_name='اسم الموقع'
    )
    # ── GPS ─────────────────────────────────────────────
    latitude = models.DecimalField(
        max_digits=10, decimal_places=7,
        null=True, blank=True, verbose_name='خط العرض'
    )
    longitude = models.DecimalField(
        max_digits=10, decimal_places=7,
        null=True, blank=True, verbose_name='خط الطول'
    )
    # ── صورة تحديد الموقع ───────────────────────────────
    location_photo = models.ImageField(
        upload_to=location_photo_path,
        null=True, blank=True,
        verbose_name='صورة تحديد الموقع'
    )
    # ── Meta ─────────────────────────────────────────────
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')
    idempotency_key = models.CharField(
        max_length=100, null=True, blank=True, unique=True,
        verbose_name='مفتاح التفرد'
    )

    class Meta:
        verbose_name = 'تقرير'
        verbose_name_plural = 'التقارير'
        ordering = ['-created_at']

    def __str__(self):
        return self.report_number

    def save(self, *args, **kwargs):
        if not self.report_number:
            self.report_number = generate_report_number()
        super().save(*args, **kwargs)

    @property
    def has_gps(self):
        return self.latitude is not None and self.longitude is not None


class ReportItem(models.Model):
    """عنصر داخل التقرير - يمثل ملاحظة/عمل واحد"""
    report = models.ForeignKey(
        Report, on_delete=models.CASCADE,
        related_name='items', verbose_name='التقرير'
    )
    note = models.ForeignKey(
        'notes.Note', on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='report_items', verbose_name='الملاحظة'
    )
    work_type = models.ForeignKey(
        'notes.WorkType', on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='report_items', verbose_name='نوع العمل'
    )
    work_item_detail = models.ForeignKey(
        'notes.WorkItemDetail', on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='report_items', verbose_name='العنصر'
    )
    work_activity = models.ForeignKey(
        'notes.WorkActivity', on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='report_items', verbose_name='النشاط'
    )
    work_classification = models.CharField(
        max_length=300, blank=True,
        verbose_name='تصنيف العمل'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')

    class Meta:
        verbose_name = 'عنصر تقرير'
        verbose_name_plural = 'عناصر التقارير'

    def __str__(self):
        wt_name = self.work_type.name if self.work_type else 'ملاحظة'
        elem_name = self.work_item_detail.name if self.work_item_detail else ''
        act_name = self.work_activity.name if self.work_activity else self.work_classification
        parts = [p for p in [wt_name, elem_name, act_name] if p]
        return f'{self.report.report_number} - ' + ' -> '.join(parts)


    @property
    def image_count(self):
        return self.images.count()


def report_image_path(instance, filename):
    """مسار حفظ الصور"""
    if instance.report_item_id and instance.report_item.report_id:
        return f'reports/{instance.report_item.report.report_number}/item_{instance.report_item.id}/{filename}'
    return f'reports/temp/{filename}'


class ReportItemImage(models.Model):
    """صور عنصر التقرير"""
    report_item = models.ForeignKey(
        ReportItem, on_delete=models.CASCADE,
        related_name='images', verbose_name='عنصر التقرير',
        null=True, blank=True
    )
    image = models.ImageField(
        upload_to=report_image_path,
        verbose_name='الصورة'
    )
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الرفع')

    class Meta:
        verbose_name = 'صورة'
        verbose_name_plural = 'الصور'
        ordering = ['uploaded_at']

    def __str__(self):
        return f'صورة {self.id} - {self.report_item}'
