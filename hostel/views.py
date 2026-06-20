from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.db.models import Count, Q
from .models import User, Room, Complaint, Notice, LeaveRequest
from .forms import (
    CustomLoginForm, StudentAddForm, StudentEditForm, RoomForm, 
    AssignRoomForm, ComplaintForm, ComplaintStatusForm, 
    LeaveRequestForm, LeaveStatusForm, NoticeForm
)

# --- AUTHORIZATION DECORATORS ---

def admin_required(view_func):
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if request.user.role == 'ADMIN':
            return view_func(request, *args, **kwargs)
        messages.error(request, "Access denied: Administrator permissions required.")
        return redirect('student_dashboard')
    return _wrapped_view

def student_required(view_func):
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if request.user.role == 'STUDENT':
            return view_func(request, *args, **kwargs)
        messages.error(request, "Access denied: Student account required.")
        return redirect('admin_dashboard')
    return _wrapped_view

# --- AUTHENTICATION VIEWS ---

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.full_name or user.username}!")
                return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = CustomLoginForm()
        
    return render(request, 'login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('login')

@login_required
def dashboard_redirect(request):
    if request.user.role == 'ADMIN':
        return redirect('admin_dashboard')
    elif request.user.role == 'STUDENT':
        return redirect('student_dashboard')
    return redirect('login')


# --- ADMIN MODULE VIEWS ---

@admin_required
def admin_dashboard(request):
    # Core statistics
    total_students = User.objects.filter(role='STUDENT').count()
    total_rooms = Room.objects.count()
    available_rooms = Room.objects.filter(status='Available').count()
    total_complaints = Complaint.objects.count()
    pending_complaints = Complaint.objects.filter(status='Pending').count()
    
    # Extra statistics for visual graphics
    resolved_complaints = Complaint.objects.filter(status='Resolved').count()
    in_progress_complaints = Complaint.objects.filter(status='In Progress').count()
    total_leaves = LeaveRequest.objects.count()
    pending_leaves = LeaveRequest.objects.filter(status='Pending').count()
    
    # Room statistics for pie chart
    full_rooms = Room.objects.filter(status='Full').count()
    partially_occupied = Room.objects.filter(occupied_count__gt=0, status='Available').count()
    vacant_rooms = Room.objects.filter(occupied_count=0).count()

    # Recent items
    recent_students = User.objects.filter(role='STUDENT').order_by('-created_at')[:5]
    recent_complaints = Complaint.objects.order_by('-created_at')[:5]
    recent_notices = Notice.objects.order_by('-created_at')[:5]

    context = {
        'total_students': total_students,
        'total_rooms': total_rooms,
        'available_rooms': available_rooms,
        'total_complaints': total_complaints,
        'pending_complaints': pending_complaints,
        'resolved_complaints': resolved_complaints,
        'in_progress_complaints': in_progress_complaints,
        'total_leaves': total_leaves,
        'pending_leaves': pending_leaves,
        
        'full_rooms': full_rooms,
        'partially_occupied': partially_occupied,
        'vacant_rooms': vacant_rooms,
        
        'recent_students': recent_students,
        'recent_complaints': recent_complaints,
        'recent_notices': recent_notices,
    }
    return render(request, 'admin/dashboard.html', context)


# Admin - Student CRUD

@admin_required
def student_list(request):
    students = User.objects.filter(role='STUDENT').order_by('-created_at')
    return render(request, 'admin/students_list.html', {'students': students})

@admin_required
def student_add(request):
    if request.method == 'POST':
        form = StudentAddForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'STUDENT'
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, f"Student '{user.full_name}' was registered successfully!")
            return redirect('student_list')
    else:
        form = StudentAddForm()
    return render(request, 'admin/student_form.html', {'form': form, 'action': 'Add New'})

@admin_required
def student_edit(request, pk):
    student = get_object_or_404(User, pk=pk, role='STUDENT')
    if request.method == 'POST':
        form = StudentEditForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, f"Student '{student.full_name}' details updated successfully!")
            return redirect('student_list')
    else:
        form = StudentEditForm(instance=student)
    return render(request, 'admin/student_form.html', {'form': form, 'action': 'Edit', 'student': student})

@admin_required
def student_delete(request, pk):
    student = get_object_or_404(User, pk=pk, role='STUDENT')
    if request.method == 'POST':
        name = student.full_name
        student.delete()
        messages.success(request, f"Student '{name}' deleted successfully.")
        return redirect('student_list')
    return render(request, 'admin/student_confirm_delete.html', {'student': student})


# Admin - Room CRUD & Allocation

@admin_required
def room_list(request):
    rooms = Room.objects.all().order_by('room_number')
    return render(request, 'admin/rooms_list.html', {'rooms': rooms})

@admin_required
def room_add(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save()
            messages.success(request, f"Room {room.room_number} added successfully!")
            return redirect('room_list')
    else:
        form = RoomForm()
    return render(request, 'admin/room_form.html', {'form': form, 'action': 'Add New'})

@admin_required
def room_edit(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            messages.success(request, f"Room {room.room_number} updated successfully!")
            return redirect('room_list')
    else:
        form = RoomForm(instance=room)
    return render(request, 'admin/room_form.html', {'form': form, 'action': 'Edit', 'room': room})

@admin_required
def room_delete(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        room_num = room.room_number
        room.delete()
        messages.success(request, f"Room {room_num} deleted successfully.")
        return redirect('room_list')
    return render(request, 'admin/room_confirm_delete.html', {'room': room})

@admin_required
def assign_room(request):
    if request.method == 'POST':
        form = AssignRoomForm(request.POST)
        if form.is_valid():
            student = form.cleaned_data['student']
            room = form.cleaned_data['room']
            
            # Save room assignment
            student.room = room
            student.save()
            messages.success(request, f"Successfully assigned Room {room.room_number} to {student.full_name}!")
            return redirect('room_list')
    else:
        form = AssignRoomForm()
    return render(request, 'admin/assign_room.html', {'form': form})


# Admin - Complaint Management

@admin_required
def admin_complaints(request):
    status_filter = request.GET.get('status')
    if status_filter in ['Pending', 'In Progress', 'Resolved']:
        complaints = Complaint.objects.filter(status=status_filter).order_by('-created_at')
    else:
        complaints = Complaint.objects.all().order_by('-created_at')
    return render(request, 'admin/complaints_list.html', {'complaints': complaints, 'current_filter': status_filter})

@admin_required
def update_complaint_status(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    if request.method == 'POST':
        form = ComplaintStatusForm(request.POST, instance=complaint)
        if form.is_valid():
            form.save()
            messages.success(request, f"Complaint status updated to '{complaint.status}' successfully!")
    return redirect('admin_complaints')


# Admin - Leave Requests Management

@admin_required
def admin_leaves(request):
    status_filter = request.GET.get('status')
    if status_filter in ['Pending', 'Approved', 'Rejected']:
        leaves = LeaveRequest.objects.filter(status=status_filter).order_by('-created_at')
    else:
        leaves = LeaveRequest.objects.all().order_by('-created_at')
    return render(request, 'admin/leaves_list.html', {'leaves': leaves, 'current_filter': status_filter})

@admin_required
def update_leave_status(request, pk):
    leave = get_object_or_404(LeaveRequest, pk=pk)
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in ['Approved', 'Rejected']:
            leave.status = status
            leave.save()
            messages.success(request, f"Leave request from {leave.student.full_name} has been {status.lower()}!")
    return redirect('admin_leaves')


# Admin - Notice Board CRUD

@admin_required
def admin_notices(request):
    notices = Notice.objects.all().order_by('-created_at')
    return render(request, 'admin/notices_list.html', {'notices': notices})

@admin_required
def notice_add(request):
    if request.method == 'POST':
        form = NoticeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Notice added to the board successfully!")
            return redirect('admin_notices')
    else:
        form = NoticeForm()
    return render(request, 'admin/notice_form.html', {'form': form, 'action': 'Add New'})

@admin_required
def notice_edit(request, pk):
    notice = get_object_or_404(Notice, pk=pk)
    if request.method == 'POST':
        form = NoticeForm(request.POST, instance=notice)
        if form.is_valid():
            form.save()
            messages.success(request, "Notice updated successfully!")
            return redirect('admin_notices')
    else:
        form = NoticeForm(instance=notice)
    return render(request, 'admin/notice_form.html', {'form': form, 'action': 'Edit', 'notice': notice})

@admin_required
def notice_delete(request, pk):
    notice = get_object_or_404(Notice, pk=pk)
    if request.method == 'POST':
        notice.delete()
        messages.success(request, "Notice deleted successfully.")
        return redirect('admin_notices')
    return render(request, 'admin/notice_confirm_delete.html', {'notice': notice})


# --- STUDENT MODULE VIEWS ---

@student_required
def student_dashboard(request):
    student = request.user
    
    # Roommates list (excluding self)
    roommates = []
    if student.room:
        roommates = User.objects.filter(room=student.room, role='STUDENT').exclude(id=student.id)
    
    # Recent notices (latest 3)
    notices = Notice.objects.all().order_by('-created_at')[:3]
    
    # Student's stats
    complaints_count = Complaint.objects.filter(student=student).count()
    pending_complaints = Complaint.objects.filter(student=student, status='Pending').count()
    approved_leaves = LeaveRequest.objects.filter(student=student, status='Approved').count()
    pending_leaves = LeaveRequest.objects.filter(student=student, status='Pending').count()

    context = {
        'student': student,
        'roommates': roommates,
        'notices': notices,
        'complaints_count': complaints_count,
        'pending_complaints': pending_complaints,
        'approved_leaves': approved_leaves,
        'pending_leaves': pending_leaves,
    }
    return render(request, 'student/dashboard.html', context)

@student_required
def student_profile(request):
    student = request.user
    if request.method == 'POST':
        # Let student edit limited profile details: full_name, email, phone
        student.full_name = request.POST.get('full_name', student.full_name)
        student.email = request.POST.get('email', student.email)
        student.phone = request.POST.get('phone', student.phone)
        student.save()
        messages.success(request, "Your profile details have been updated successfully!")
        return redirect('student_profile')
    return render(request, 'student/profile.html', {'student': student})

@student_required
def student_room_details(request):
    student = request.user
    roommates = []
    if student.room:
        roommates = User.objects.filter(room=student.room, role='STUDENT').exclude(id=student.id)
    return render(request, 'student/room_details.html', {'room': student.room, 'roommates': roommates})

@student_required
def student_complaints(request):
    student = request.user
    complaints = Complaint.objects.filter(student=student).order_by('-created_at')
    
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.student = student
            complaint.save()
            messages.success(request, "Your complaint has been submitted successfully!")
            return redirect('student_complaints')
    else:
        form = ComplaintForm()

    return render(request, 'student/complaints.html', {
        'complaints': complaints,
        'form': form
    })

@student_required
def student_leave_requests(request):
    student = request.user
    leaves = LeaveRequest.objects.filter(student=student).order_by('-created_at')
    
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.student = student
            leave.save()
            messages.success(request, "Your leave application has been submitted successfully!")
            return redirect('student_leave_requests')
    else:
        form = LeaveRequestForm()

    return render(request, 'student/leave_requests.html', {
        'leaves': leaves,
        'form': form
    })

@student_required
def student_notices(request):
    notices = Notice.objects.all().order_by('-created_at')
    return render(request, 'student/notices.html', {'notices': notices})
