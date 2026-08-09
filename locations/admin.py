from django.contrib import admin
from .models import Unit, LocationType, Location


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name']


@admin.register(LocationType)
class LocationTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name']


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'unit', 'location_type', 'is_active']
    list_filter = ['unit', 'location_type', 'is_active']
    search_fields = ['name']
