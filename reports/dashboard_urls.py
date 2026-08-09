from django.urls import path
from . import dashboard_views

app_name = 'dashboard'

urlpatterns = [
    path('', dashboard_views.DashboardHomeView.as_view(), name='home'),
    # Users (Contractors)
    path('users/', dashboard_views.UserListView.as_view(), name='user_list'),
    path('users/create/', dashboard_views.UserCreateView.as_view(), name='user_create'),
    path('users/<int:pk>/edit/', dashboard_views.UserUpdateView.as_view(), name='user_edit'),
    path('users/<int:pk>/delete/', dashboard_views.UserDeleteView.as_view(), name='user_delete'),
    # Supervisors (المراقبين)
    path('supervisors/', dashboard_views.SupervisorListView.as_view(), name='supervisor_list'),
    path('supervisors/create/', dashboard_views.SupervisorCreateView.as_view(), name='supervisor_create'),
    path('supervisors/<int:pk>/edit/', dashboard_views.SupervisorUpdateView.as_view(), name='supervisor_edit'),
    path('supervisors/<int:pk>/delete/', dashboard_views.SupervisorDeleteView.as_view(), name='supervisor_delete'),
    # Units
    path('units/', dashboard_views.UnitListView.as_view(), name='unit_list'),
    path('units/create/', dashboard_views.UnitCreateView.as_view(), name='unit_create'),
    path('units/<int:pk>/edit/', dashboard_views.UnitUpdateView.as_view(), name='unit_edit'),
    path('units/<int:pk>/delete/', dashboard_views.UnitDeleteView.as_view(), name='unit_delete'),
    # Location Types
    path('location-types/', dashboard_views.LocationTypeListView.as_view(), name='locationtype_list'),
    path('location-types/create/', dashboard_views.LocationTypeCreateView.as_view(), name='locationtype_create'),
    path('location-types/<int:pk>/edit/', dashboard_views.LocationTypeUpdateView.as_view(), name='locationtype_edit'),
    path('location-types/<int:pk>/delete/', dashboard_views.LocationTypeDeleteView.as_view(), name='locationtype_delete'),
    # Work Types
    path('work-types/', dashboard_views.WorkTypeListView.as_view(), name='worktype_list'),
    path('work-types/create/', dashboard_views.WorkTypeCreateView.as_view(), name='worktype_create'),
    path('work-types/<int:pk>/edit/', dashboard_views.WorkTypeUpdateView.as_view(), name='worktype_edit'),
    path('work-types/<int:pk>/delete/', dashboard_views.WorkTypeDeleteView.as_view(), name='worktype_delete'),
    # Work Item Details (العناصر)
    path('work-items/', dashboard_views.WorkItemDetailListView.as_view(), name='workitem_list'),
    path('work-items/create/', dashboard_views.WorkItemDetailCreateView.as_view(), name='workitem_create'),
    path('work-items/<int:pk>/edit/', dashboard_views.WorkItemDetailUpdateView.as_view(), name='workitem_edit'),
    path('work-items/<int:pk>/delete/', dashboard_views.WorkItemDetailDeleteView.as_view(), name='workitem_delete'),
    # Work Activities (الأنشطة)
    path('work-activities/create/', dashboard_views.WorkActivityCreateView.as_view(), name='workactivity_create'),
    path('work-activities/<int:pk>/edit/', dashboard_views.WorkActivityUpdateView.as_view(), name='workactivity_edit'),
    path('work-activities/<int:pk>/delete/', dashboard_views.WorkActivityDeleteView.as_view(), name='workactivity_delete'),
    # Locations
    path('locations/', dashboard_views.LocationListView.as_view(), name='location_list'),
    path('locations/create/', dashboard_views.LocationCreateView.as_view(), name='location_create'),
    path('locations/<int:pk>/edit/', dashboard_views.LocationUpdateView.as_view(), name='location_edit'),
    path('locations/<int:pk>/delete/', dashboard_views.LocationDeleteView.as_view(), name='location_delete'),
    # Notes
    path('notes/', dashboard_views.NoteListView.as_view(), name='note_list'),
    path('notes/create/', dashboard_views.NoteCreateView.as_view(), name='note_create'),
    path('notes/<int:pk>/edit/', dashboard_views.NoteUpdateView.as_view(), name='note_edit'),
    path('notes/<int:pk>/delete/', dashboard_views.NoteDeleteView.as_view(), name='note_delete'),
    # Indicators & Reports
    path('indicators/', dashboard_views.WorkIndicatorsView.as_view(), name='indicators'),
    path('reports/', dashboard_views.ReportListView.as_view(), name='report_list'),
    path('reports/<int:pk>/', dashboard_views.ReportDetailView.as_view(), name='report_detail'),
    path('reports/<int:pk>/delete/', dashboard_views.ReportDeleteView.as_view(), name='report_delete'),
    path('reports/export/excel/', dashboard_views.ExportExcelView.as_view(), name='export_excel'),
    path('reports/export/bulk-pdf/', dashboard_views.BulkExportPDFView.as_view(), name='report_bulk_export_pdf'),
    path('reports/<int:pk>/export/pdf/', dashboard_views.ExportPDFView.as_view(), name='export_pdf'),
]
