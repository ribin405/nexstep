from django.urls import path
from . import views

urlpatterns = [
    # --- COMMON & AUTHENTICATION ---
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_redirect, name='dashboard'),

    # --- ADMIN MODULE ROUTES ---
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    # Admin - Student CRUD
    path('admin/students/', views.student_list, name='student_list'),
    path('admin/students/add/', views.student_add, name='student_add'),
    path('admin/students/<int:pk>/edit/', views.student_edit, name='student_edit'),
    path('admin/students/<int:pk>/delete/', views.student_delete, name='student_delete'),
    
    # Admin - Room CRUD & Allocation
    path('admin/rooms/', views.room_list, name='room_list'),
    path('admin/rooms/add/', views.room_add, name='room_add'),
    path('admin/rooms/<int:pk>/edit/', views.room_edit, name='room_edit'),
    path('admin/rooms/<int:pk>/delete/', views.room_delete, name='room_delete'),
    path('admin/rooms/assign/', views.assign_room, name='assign_room'),
    
    # Admin - Complaint Management
    path('admin/complaints/', views.admin_complaints, name='admin_complaints'),
    path('admin/complaints/<int:pk>/update/', views.update_complaint_status, name='update_complaint_status'),
    
    # Admin - Leave Requests Management
    path('admin/leaves/', views.admin_leaves, name='admin_leaves'),
    path('admin/leaves/<int:pk>/update/', views.update_leave_status, name='update_leave_status'),
    
    # Admin - Notice Board CRUD
    path('admin/notices/', views.admin_notices, name='admin_notices'),
    path('admin/notices/add/', views.notice_add, name='notice_add'),
    path('admin/notices/<int:pk>/edit/', views.notice_edit, name='notice_edit'),
    path('admin/notices/<int:pk>/delete/', views.notice_delete, name='notice_delete'),

    # --- STUDENT MODULE ROUTES ---
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student/profile/', views.student_profile, name='student_profile'),
    path('student/room/', views.student_room_details, name='student_room_details'),
    path('student/complaints/', views.student_complaints, name='student_complaints'),
    path('student/leaves/', views.student_leave_requests, name='student_leave_requests'),
    path('student/notices/', views.student_notices, name='student_notices'),
]
