from django.urls import path
from . import views
from student.views import library_view

urlpatterns = [
    path('dashboard/', views.lecturer_dashboard, name='lecturer_dashboard'),
    path('upload-student/', views.upload_csv, name='upload_csv'),
    path('upload-material/', views.upload_material, name='upload_material'),
    path('materials/', views.material_list, name='material_list'),
    path('class-select/', views.select_classes, name='select_class'),
    path('supervisor-dashboard/', views.supervisor_dashboard, name='supervisor_dashboard'),
    path('approve-request/<int:request_id>/', views.approve_request, name='approve_request'),
    path('library/', library_view, name='library'),
    path('upload-report', views.library_upload, name='upload_report')
]