from django.urls import path
from . import views
from .views import PatientRecordsView, EmotionLogView, EmotionLogChartView

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('signup/', views.register_view, name='signup'),  # Registration page
    path('login/', views.login_view, name='login'),  # Login page
    path('logout/', views.logout_view, name='logout'),  # Logout functionality
    path('doctor-dashboard/', views.doctor_dashboard, name='doctor_dashboard'),  # Doctor's dashboard
    path('patient-dashboard/', views.patient_dashboard, name='patient_dashboard'),  # Patient's dashboard
    path('patient-records/', PatientRecordsView.as_view(), name='patient-records'),  # View patient records
    path('emotion-logs/', EmotionLogView.as_view(), name='emotion-logs'),  # View recent emotion logs
    path('emotion-log-chart/<int:days>/', EmotionLogChartView.as_view(), name='emotion-log-chart'),  # View emotion log chart
]

    

 

