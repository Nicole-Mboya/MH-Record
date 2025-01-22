from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from rest_framework.response import Response
from django.db import models
from .models import Appointment, AppointmentNote, Patient, EmotionLog, Register
from .serializers import AppointmentSerializer, AppointmentNoteSerializer, PatientRecordSerializer, EmotionLogSerializer, JournalEntrySerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, Group, Permission
from rest_framework import status
from rest_framework.decorators import api_view

def home(request):
    return render(request='home.html')

@api_view(['POST'])
def register_view(request):
    if request.method == 'POST':
        data = request.data
        try:
            user = Register.objects.create_user(
                username=data['username'],
                password=data['password'],
                email=data['email'],
                role = user.role if user.role else 'patient'

            )
            user.save()  # This will trigger the save method in Register to assign them to the correct group
            return Response({"message": "User created successfully!"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)  # Start session
            # Redirect based on role
            if user.role == 'doctor':
                return JsonResponse({'redirect_url': '/doctor-dashboard/'})
            elif user.role == 'patient':
                return JsonResponse({'redirect_url': '/patient-dashboard/'})
            return JsonResponse({'redirect_url': '/'})  # Default fallback
        return JsonResponse({'error': 'Invalid credentials'}, status=401)

    return render(request, 'login.html')

# Doctor's Dashboard view
@login_required
def doctor_dashboard(request):
    return render(request, 'doctor_dashboard.html')

# Patient's Dashboard view
@login_required
def patient_dashboard(request):
    return render(request, 'patient_dashboard.html')

class PatientRecordsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        
        if not user.is_authenticated:
            return Response({"error": "Authentication required."}, status=401)

        # Get all patients assigned to this doctor
        patients = Patient.objects.all()  # You can filter this based on the doctor's permissions
        
        patient_records = []
        for patient in patients:
            appointments = Appointment.objects.filter(patient=patient)
            notes = AppointmentNote.objects.filter(appointment__in=appointments)
            mental_health_history = MentalHealthHistory.objects.filter(patient=patient)
            
            patient_data = {
                'patient_id': patient.id,
                'patient_name': patient.user.username,
                'age': patient.age,
                'gender': patient.gender,
                'appointments': appointments.values('id', 'date', 'is_cancelled'),
                'notes': notes.values('note'),
                'mental_health_history': mental_health_history.values('date_recorded', 'mental_health_status')
            }
            patient_records.append(patient_data)

        return Response(patient_records)

class EmotionLogView(APIView):
    def get(self, request):
        """Return the last 3 emotion logs of the patient"""
        logs = EmotionLog.objects.filter(patient=request.user).order_by('-created_at')[:3]
        log_data = [{'emotion': log.emotion, 'created_at': log.created_at} for log in logs]
        return Response(log_data, status=200)

class EmotionLogChartView(APIView):
    def get(self, request, days=7):
        """Fetch emotion log data for the last 7 or 30 days"""
        end_date = timezone.now()
        start_date = end_date - timedelta(days=days)

        # Get emotion logs for the logged-in user
        logs = EmotionLog.objects.filter(
            patient=request.user, 
            created_at__gte=start_date,
            created_at__lte=end_date
        ).values('emotion', 'created_at__date')

        emotion_data = {}
        for log in logs:
            date = log['created_at__date']
            emotion = log['emotion']
            if date not in emotion_data:
                emotion_data[date] = {}
            if emotion not in emotion_data[date]:
                emotion_data[date][emotion] = 0
            emotion_data[date][emotion] += 1

        chart_data = {
            'labels': [],
            'datasets': []
        }

        emotions = set([log['emotion'] for log in logs])
        for emotion in emotions:
            dataset = {
                'label': emotion,
                'data': [],
                'backgroundColor': 'rgba(75, 192, 192, 0.2)',
                'borderColor': 'rgba(75, 192, 192, 1)',
                'borderWidth': 1
            }
            for date in sorted(emotion_data.keys()):
                chart_data['labels'].append(date)
                dataset['data'].append(emotion_data[date].get(emotion, 0))
            chart_data['datasets'].append(dataset)

        return Response(chart_data, status=200)
