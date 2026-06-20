from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver

class Room(models.Model):
    STATUS_CHOICES = (
        ('Available', 'Available'),
        ('Full', 'Full'),
    )
    room_number = models.CharField(max_length=20, unique=True)
    capacity = models.IntegerField()
    occupied_count = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Available')

    def save(self, *args, **kwargs):
        # Recalculate occupied count based on actual students in the database
        if self.pk:
            self.occupied_count = self.students.count()
        
        # Determine availability status
        if self.occupied_count >= self.capacity:
            self.status = 'Full'
        else:
            self.status = 'Available'
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Room {self.room_number} ({self.occupied_count}/{self.capacity})"


class User(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('STUDENT', 'Student'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='STUDENT')
    full_name = models.CharField(max_length=150, blank=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    gender = models.CharField(
        max_length=10, 
        choices=(('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')), 
        blank=True, 
        null=True
    )
    course = models.CharField(max_length=100, blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Keep Django's first_name and last_name in sync with full_name
        if self.full_name:
            parts = self.full_name.split(' ', 1)
            self.first_name = parts[0]
            if len(parts) > 1:
                self.last_name = parts[1]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name if self.full_name else self.username


class Complaint(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
    )
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'STUDENT'}, related_name='complaints')
    subject = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} - {self.student.username} ({self.status})"


class Notice(models.Model):
    title = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class LeaveRequest(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'STUDENT'}, related_name='leave_requests')
    from_date = models.DateField()
    to_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Leave Request - {self.student.username} ({self.status})"


# --- SIGNALS FOR ROOM OCCUPANCY TRACKING ---

@receiver(pre_save, sender=User)
def track_old_room(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = User.objects.get(pk=instance.pk)
            instance._old_room = old_instance.room
        except User.DoesNotExist:
            instance._old_room = None
    else:
        instance._old_room = None


@receiver(post_save, sender=User)
def update_room_occupancy_on_save(sender, instance, created, **kwargs):
    if instance.role == 'STUDENT':
        old_room = getattr(instance, '_old_room', None)
        new_room = instance.room
        
        # If room was changed or assigned
        if old_room != new_room:
            if old_room:
                old_room.save()  # Triggers Room.save() to recount students
            if new_room:
                new_room.save()  # Triggers Room.save() to recount students
        else:
            if new_room:
                new_room.save()


@receiver(post_delete, sender=User)
def update_room_occupancy_on_delete(sender, instance, **kwargs):
    if instance.role == 'STUDENT' and instance.room:
        room = instance.room
        room.save()  # Recounts occupied students and recalculates status
