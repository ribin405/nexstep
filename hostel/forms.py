import re
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User, Room, Complaint, Notice, LeaveRequest

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Username', 'autofocus': True})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'})
    )


class StudentAddForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'}), 
        required=True
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}), 
        required=True
    )

    class Meta:
        model = User
        fields = ['username', 'full_name', 'email', 'phone', 'gender', 'course', 'year', 'room']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show rooms that have space
        self.fields['room'].queryset = Room.objects.filter(status='Available')
        self.fields['room'].empty_label = "Select/Assign Room (Optional)"
        
        # Add styling to fields
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            if name == 'gender':
                field.widget.attrs.update({'class': 'form-select'})

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            # simple validation: digits only, length between 10 and 15
            if not re.match(r'^\d{10,15}$', phone):
                raise forms.ValidationError("Enter a valid phone number (10 to 15 digits).")
        return phone

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")
        
        return cleaned_data


class StudentEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['full_name', 'email', 'phone', 'gender', 'course', 'year', 'room']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Room choices include Available rooms plus the current assigned room of this student
        current_room_id = self.instance.room_id if self.instance else None
        self.fields['room'].queryset = Room.objects.filter(status='Available') | Room.objects.filter(pk=current_room_id)
        self.fields['room'].empty_label = "No Room Assigned"
        
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            if name == 'gender':
                field.widget.attrs.update({'class': 'form-select'})

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            if not re.match(r'^\d{10,15}$', phone):
                raise forms.ValidationError("Enter a valid phone number (10 to 15 digits).")
        return phone


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_number', 'capacity']
        widgets = {
            'room_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Room Number'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Capacity', 'min': 1}),
        }

    def clean_capacity(self):
        capacity = self.cleaned_data.get('capacity')
        if capacity is not None and capacity <= 0:
            raise forms.ValidationError("Room capacity must be greater than 0.")
        return capacity


class AssignRoomForm(forms.Form):
    student = forms.ModelChoiceField(
        queryset=User.objects.filter(role='STUDENT'),
        label="Select Student",
        empty_label="Choose a student",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    room = forms.ModelChoiceField(
        queryset=Room.objects.filter(status='Available'),
        label="Select Available Room",
        empty_label="Choose a room",
        widget=forms.Select(attrs={'class': 'form-select'})
    )


class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['subject', 'description']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter complaint subject...'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Provide detailed explanation of the issue...'}),
        }


class ComplaintStatusForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
        }


class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['from_date', 'to_date', 'reason']
        widgets = {
            'from_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'to_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'State the reason for leave...'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        from_date = cleaned_data.get('from_date')
        to_date = cleaned_data.get('to_date')

        if from_date and to_date and from_date > to_date:
            self.add_error('to_date', "End date cannot be before the start date.")
        
        return cleaned_data


class LeaveStatusForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
        }


class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['title', 'message']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter notice title...'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Write notice message...'}),
        }
