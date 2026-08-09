from django.db import models
from django.contrib.auth.models import User
from locations.models import Unit


class UserProfile(models.Model):
    """بروفايل المستخدم - يربط كل مستخدم بوحدة واحدة ونوع الحساب (مقاول / مراقب)"""
    ROLE_CHOICES = (
        ('contractor', 'مقاول'),
        ('supervisor', 'مراقب'),
    )

    user = models.OneToOneField(
        User, on_delete=models.CASCADE,
        related_name='profile', verbose_name='المستخدم'
    )
    unit = models.ForeignKey(
        Unit, on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='user_profiles', verbose_name='وحدة التنسيق'
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='contractor',
        verbose_name='نوع المستخدم'
    )

    class Meta:
        verbose_name = 'بروفايل مستخدم'
        verbose_name_plural = 'بروفايلات المستخدمين'

    def __str__(self):
        return f'{self.user.username} ({self.get_role_display()}) - {self.unit.name if self.unit else "بدون وحدة"}'
