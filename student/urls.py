from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('milestone/', views.milestone_list, name='milestone_list'),
    path('milestone/add/', views.milestone_add, name='milestone_add'),
    path('milestone/edit/<int:pk>/', views.milestone_edit, name='milestone_edit'),
    path('milestone/delete/<int:pk>/', views.milestone_delete, name='milestone_delete'),
    path('milestone/toggle/<int:pk>/', views.milestone_toggle, name='milestone_toggle'),
    path('submission/', views.submission_view, name='submission'),
    path('submission/<int:submission_id>/', views.submission_detail, name='submission_detail'),
    path('supervisor-request/', views.supervisor_request_view, name='supervisor_request'),
    path('profile/', views.student_profile_view, name='profile'),
    path('library/', views.library_view, name='library'),
    path('save-notes/', views.save_notes, name='save_notes'),
]