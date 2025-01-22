from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from datetime import timedelta
from django.utils import timezone
from .models import (
    Appointment, AppointmentNote, Patient, EmotionLog, Register, MentalHealthHistory
)
from .serializers import (
    AppointmentSerializer, AppointmentNoteSerializer, PatientRecordSerializer,
    EmotionLogSerializer, JournalEntrySerializer
)
import logging

# Logger setup
logger = logging.getLogger(__name__)

# Home View
def home(request):
    return render(request, 'index.html')

# Registration View (API)
@api_view(['POST'])
def register_view(request):
    data = request.data
    try:
        # Create a new user instance with role
        new_user = Register.objects.create_user(
            username=data['username'],
            password=data['password'],
            email=data['email'],
            role=data.get('role', 'patient')  # Default role is 'patient'
        )
        return Response({"message": "User created successfully!"}, status=status.HTTP_201_CREATED)
    except Exception as e:
        logger.error(f"Error during registration: {e}")
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Login View (handles POST requests)
@csrf_exempt  # To handle CSRF issues, you can remove this if you're using CSRF tokens.
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        logger.info(f"Attempting login for username: {username}")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            logger.info(f"Login successful for username: {username}")

            # Redirect based on user role
            if hasattr(user, 'role'):
                if user.role == 'doctor':
                    return JsonResponse({'redirect_url': '/doctor-dashboard/'})
                elif user.role == 'patient':
                    return JsonResponse({'redirect_url': '/patient-dashboard/'})
            return JsonResponse({'redirect_url': '/'})  # Default fallback for other roles
        else:
            logger.warning(f"Login failed for username: {username}")
            return JsonResponse({'error': 'Invalid credentials'}, status=401)

    return render(request, 'login.html')

# Logout View (for logged-in users)
@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')  # Redirect to home after logout

# Doctor Dashboard View
@login_required
def doctor_dashboard(request):
    return render(request, 'doctor_dashboard.html')

# Patient Dashboard View
@login_required
def patient_dashboard(request):
    return render(request, 'patient_dashboard.html')

# Patient Records View
class PatientRecordsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if not user.is_authenticated:
            return Response({"error": "Authentication required."}, status=401)

        # Fetch all patients (can be filtered based on permissions or doctor assignment)
        patients = Patient.objects.all()
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
                'mental_health_history': mental_health_history.values('date_recorded', 'mental_health_status'),
            }
            patient_records.append(patient_data)

        return Response(patient_records)

# Emotion Log View
class EmotionLogView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logs = EmotionLog.objects.filter(patient=request.user).order_by('-created_at')[:3]
        log_data = [{'emotion': log.emotion, 'created_at': log.created_at} for log in logs]
        return Response(log_data, status=200)

# Emotion Log Chart View
class EmotionLogChartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, days=7):
        end_date = timezone.now()
        start_date = end_date - timedelta(days=days)

        logs = EmotionLog.objects.filter(
            patient=request.user,
            created_at__range=(start_date, end_date)
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
            'labels': sorted(emotion_data.keys()),
            'datasets': []
        }

        all_emotions = set([log['emotion'] for log in logs])
        for emotion in all_emotions:
            dataset = {
                'label': emotion,
                'data': [emotion_data[date].get(emotion, 0) for date in sorted(emotion_data.keys())],
                'backgroundColor': 'rgba(75, 192, 192, 0.2)',
                'borderColor': 'rgba(75, 192, 192, 1)',
                'borderWidth': 1
            }
            chart_data['datasets'].append(dataset)

        return Response(chart_data, status=200)
