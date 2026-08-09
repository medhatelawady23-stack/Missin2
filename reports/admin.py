from django.contrib import admin
from .models import Report, ReportItem, ReportItemImage


class ReportItemImageInline(admin.TabularInline):
    model = ReportItemImage
    extra = 0
    readonly_fields = ['uploaded_at']


class ReportItemInline(admin.TabularInline):
    model = ReportItem
    extra = 0
    readonly_fields = ['created_at']


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['report_number', 'user', 'unit', 'location', 'created_at']
    list_filter = ['unit', 'location_type', 'created_at']
    search_fields = ['report_number', 'user__username', 'location__name']
    readonly_fields = ['report_number', 'created_at']
    inlines = [ReportItemInline]


@admin.register(ReportItem)
class ReportItemAdmin(admin.ModelAdmin):
    list_display = ['report', 'note', 'image_count', 'created_at']
    list_filter = ['note']
    inlines = [ReportItemImageInline]
