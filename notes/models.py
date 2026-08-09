from django.db import models
from locations.models import Location


class WorkType(models.Model):
    """نوع العمل - يُدار من لوحة التحكم"""
    CATEGORY_CHOICES = [
        ('restroom', 'دورات المياه'),
        ('location', 'مواقع'),
        ('open_space', 'مساحات انتشارية'),
    ]

    name = models.CharField(max_length=200, verbose_name='نوع العمل')
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='location',
        verbose_name='تصنيف الموقع'
    )
    is_active = models.BooleanField(default=True, verbose_name='نشط')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')

    class Meta:
        verbose_name = 'نوع عمل'
        verbose_name_plural = 'أنواع العمل'
        ordering = ['name']
        unique_together = ('name', 'category')

    def __str__(self):
        return self.name


class WorkItemDetail(models.Model):
    """المستوى الثاني: العنصر - التابع لنوع العمل"""
    work_type = models.ForeignKey(
        WorkType,
        on_delete=models.CASCADE,
        related_name='details',
        verbose_name='نوع العمل'
    )
    name = models.CharField(max_length=250, verbose_name='اسم العنصر')
    is_active = models.BooleanField(default=True, verbose_name='نشط')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')

    class Meta:
        verbose_name = 'عنصر'
        verbose_name_plural = 'العناصر'
        ordering = ['work_type', 'name']

    def __str__(self):
        return f'{self.work_type.name} - {self.name}'


class WorkActivity(models.Model):
    """المستوى الثالث: النشاط - التابع للعنصر"""
    element = models.ForeignKey(
        WorkItemDetail,
        on_delete=models.CASCADE,
        related_name='activities',
        verbose_name='العنصر'
    )
    name = models.CharField(max_length=250, verbose_name='اسم النشاط')
    is_active = models.BooleanField(default=True, verbose_name='نشط')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')

    class Meta:
        verbose_name = 'نشاط'
        verbose_name_plural = 'الأنشطة'
        ordering = ['element', 'name']

    def __str__(self):
        return f'{self.element.name} - {self.name}'


class Note(models.Model):
    """الملاحظة الجاهزة - مثل: تشققات، دهانات تالفة، نظافة"""
    text = models.CharField(max_length=300, verbose_name='نص الملاحظة')
    locations = models.ManyToManyField(
        Location,
        through='NoteLocation',
        related_name='notes',
        blank=True,
        verbose_name='المواقع المرتبطة'
    )
    is_active = models.BooleanField(default=True, verbose_name='نشط')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')

    class Meta:
        verbose_name = 'ملاحظة'
        verbose_name_plural = 'الملاحظات'
        ordering = ['text']

    def __str__(self):
        return self.text


class NoteLocation(models.Model):
    """جدول الربط بين الملاحظات والمواقع"""
    note = models.ForeignKey(Note, on_delete=models.CASCADE, verbose_name='الملاحظة')
    location = models.ForeignKey(Location, on_delete=models.CASCADE, verbose_name='الموقع')

    class Meta:
        verbose_name = 'ملاحظة موقع'
        verbose_name_plural = 'ملاحظات المواقع'
        unique_together = ['note', 'location']

    def __str__(self):
        return f'{self.note.text} ← {self.location.name}'
