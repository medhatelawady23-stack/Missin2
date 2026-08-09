from django.contrib import admin
from .models import Note, NoteLocation, WorkType, WorkItemDetail, WorkActivity


@admin.register(WorkType)
class WorkTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'is_active', 'created_at']
    list_filter = ['category', 'is_active']
    search_fields = ['name']


@admin.register(WorkItemDetail)
class WorkItemDetailAdmin(admin.ModelAdmin):
    list_display = ['name', 'work_type', 'is_active', 'created_at']
    list_filter = ['work_type', 'is_active']
    search_fields = ['name', 'work_type__name']


@admin.register(WorkActivity)
class WorkActivityAdmin(admin.ModelAdmin):
    list_display = ['name', 'element', 'is_active', 'created_at']
    list_filter = ['element__work_type', 'element', 'is_active']
    search_fields = ['name', 'element__name']


class NoteLocationInline(admin.TabularInline):
    model = NoteLocation
    extra = 1


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['text', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['text']
    inlines = [NoteLocationInline]
