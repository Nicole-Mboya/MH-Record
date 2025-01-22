from rest_framework import serializers
from .models import Appointment, AppointmentNote, MentalHealthHistory, Patient, EmotionLog, JournalEntry

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 'date', 'is_cancelled']

class AppointmentNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppointmentNote
        fields = ['note']

class MentalHealthHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MentalHealthHistory
        fields = ['date_recorded', 'mental_health_status']

class PatientRecordSerializer(serializers.Serializer):
    patient_id = serializers.IntegerField()
    patient_name = serializers.CharField()
    age = serializers.IntegerField()
    gender = serializers.CharField()
    appointments = AppointmentSerializer(many=True)
    notes = AppointmentNoteSerializer(many=True)
    mental_health_history = MentalHealthHistorySerializer(many=True)

class EmotionLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmotionLog
        fields = ['id', 'emotion', 'created_at']

class JournalEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = JournalEntry
        fields = ['id', 'text_content', 'image', 'created_at']
