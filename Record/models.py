from django.db import models

from django.db import models

from django.contrib.auth.models import AbstractUser, Group, Permission

class Register(AbstractUser):
    role = models.CharField(max_length=10, choices=[('doctor', 'Doctor'), ('patient', 'Patient')])

    # Explicitly set the related_name to avoid clashes
    groups = models.ManyToManyField(
        Group,
        related_name='register_users',  # Change this to avoid clashes
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='register_users',  # Change this to avoid clashes
        blank=True
    )

    def save(self, *args, **kwargs):
        # Automatically add the user to the correct group based on their role
        if not self.pk:  # This is a new user
            if self.role == 'doctor':
                doctor_group, created = Group.objects.get_or_create(name='doctor')
                self.groups.add(doctor_group)
            elif self.role == 'patient':
                patient_group, created = Group.objects.get_or_create(name='patient')
                self.groups.add(patient_group)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.username



class User(AbstractUser):
    role = models.CharField(max_length=10, choices=[('doctor', 'Doctor'), ('patient', 'Patient')], default='patient')

    # Override groups field with custom related_name to avoid conflict
    groups = models.ManyToManyField(
        Group,
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='custom_user_groups'  # Changed related_name
    )

    # Override user_permissions field with custom related_name to avoid conflict
    user_permissions = models.ManyToManyField(
        Permission,
        blank=True,
        help_text='Specific permissions for the user.',
        related_name='custom_user_permissions'  # Changed related_name
    )

    def save(self, *args, **kwargs):
        # Automatically assign user to the appropriate group based on their role
        if not self.pk:  # This check ensures the user is newly created
            if self.role == 'doctor':
                doctor_group, created = Group.objects.get_or_create(name='doctor')
                self.groups.add(doctor_group)
            elif self.role == 'patient':
                patient_group, created = Group.objects.get_or_create(name='patient')
                self.groups.add(patient_group)
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username



class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1) 
    age = models.IntegerField(default=0)  # Add a default value for age
    gender = models.CharField(max_length=10, default='unknown') 
    # Add other patient details as needed

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField()
    is_cancelled = models.BooleanField(default=False)

class AppointmentNote(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    note = models.TextField()

class MentalHealthHistory(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date_recorded = models.DateField()
    mental_health_status = models.TextField()

class EmotionLog(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='emotion_logs')
    emotion = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.username} - {self.emotion}"

class JournalEntry(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    text_content = models.TextField()
    image = models.ImageField(upload_to='journals/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Journal by {self.patient.username} - {self.created_at}"
