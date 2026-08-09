from django.db import models


class Unit(models.Model):
    """وحدة التنسيق - مثل: بلدية الرياض، بلدية جدة"""
    name = models.CharField(max_length=200, unique=True, verbose_name='اسم وحدة التنسيق')
    description = models.TextField(blank=True, verbose_name='الوصف')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')
    is_active = models.BooleanField(default=True, verbose_name='نشط')

    class Meta:
        verbose_name = 'وحدة تنسيق'
        verbose_name_plural = 'وحدات التنسيق'
        ordering = ['name']

    def __str__(self):
        return self.name


class LocationType(models.Model):
    """تصنيف الموقع - مثل: مبنى، حديقة، شارع، مستودع"""
    name = models.CharField(max_length=200, unique=True, verbose_name='تصنيف الموقع')
    description = models.TextField(blank=True, verbose_name='الوصف')
    is_active = models.BooleanField(default=True, verbose_name='نشط')

    class Meta:
        verbose_name = 'تصنيف موقع'
        verbose_name_plural = 'تصنيفات المواقع'
        ordering = ['name']

    def __str__(self):
        return self.name


class Location(models.Model):
    """الموقع - مرتبط بوحدة تنسيق وتصنيف موقع"""
    name = models.CharField(max_length=200, verbose_name='اسم الموقع')
    unit = models.ForeignKey(
        Unit, on_delete=models.CASCADE,
        related_name='locations', verbose_name='وحدة التنسيق'
    )
    location_type = models.ForeignKey(
        LocationType, on_delete=models.CASCADE,
        related_name='locations', verbose_name='تصنيف الموقع'
    )
    address = models.TextField(blank=True, verbose_name='العنوان')
    is_active = models.BooleanField(default=True, verbose_name='نشط')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')

    class Meta:
        verbose_name = 'موقع'
        verbose_name_plural = 'المواقع'
        ordering = ['unit', 'name']
        unique_together = ['name', 'unit']

    def __str__(self):
        return f'{self.name} - {self.unit.name}'
