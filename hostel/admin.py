from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Room, Complaint, Notice, LeaveRequest

class CustomUserAdmin(UserAdmin):
    model = User
    fieldsets = UserAdmin.fieldsets + (
        ('Hostel Details', {'fields': ('role', 'full_name', 'phone', 'gender', 'course', 'year', 'room')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Hostel Details', {'fields': ('role', 'full_name', 'phone', 'gender', 'course', 'year', 'room')}),
    )
    list_display = ['username', 'email', 'full_name', 'role', 'room', 'is_staff']
    list_filter = ['role', 'gender', 'course', 'year']
    search_fields = ['username', 'email', 'full_name', 'phone']

class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_number', 'capacity', 'occupied_count', 'status']
    list_filter = ['status']
    search_fields = ['room_number']

class ComplaintAdmin(admin.ModelAdmin):
    list_display = ['student', 'subject', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['subject', 'description', 'student__username', 'student__full_name']

class NoticeAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at']
    search_fields = ['title', 'message']

class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ['student', 'from_date', 'to_date', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['reason', 'student__username', 'student__full_name']

# Register models
admin.site.register(User, CustomUserAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Complaint, ComplaintAdmin)
admin.site.register(Notice, NoticeAdmin)
admin.site.register(LeaveRequest, LeaveRequestAdmin)
