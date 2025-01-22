from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

class Register(AbstractUser):
    role = models.CharField(max_length=10, choices=[('doctor', 'Doctor'), ('patient', 'Patient')])

    groups = models.ManyToManyField(
        Group,
        related_name='register_users',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='register_users',
        blank=True
    )

    def __str__(self):
        return self.username


@receiver(post_save, sender=Register)
def assign_group(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'doctor':
            doctor_group, created = Group.objects.get_or_create(name='doctor')
            instance.groups.add(doctor_group)
        elif instance.role == 'patient':
            patient_group, created = Group.objects.get_or_create(name='patient')
            instance.groups.add(patient_group)
        instance.save()

# Use Register instead of User for the Patient model
class Patient(models.Model):
    user = models.OneToOneField(Register, on_delete=models.CASCADE)  # Changed to Register
    age = models.IntegerField(default=0)
    gender = models.CharField(max_length=10, default='unknown')

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Register, on_delete=models.CASCADE)  # Changed to Register
    date = models.DateTimeField()
    is_cancelled = models.BooleanField(default=False)

class AppointmentNote(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    note = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

class MentalHealthHistory(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date_recorded = models.DateField()
    mental_health_status = models.TextField()

class EmotionLog(models.Model):
    patient = models.ForeignKey(Register, on_delete=models.CASCADE, related_name='emotion_logs')  # Changed to Register
    emotion = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.patient.username} - {self.emotion}"

class JournalEntry(models.Model):
    patient = models.ForeignKey(Register, on_delete=models.CASCADE)  # Changed to Register
    text_content = models.TextField()
    image = models.ImageField(upload_to='journals/', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Journal by {self.patient.username} - {self.created_at}"
