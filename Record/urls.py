from django.urls import path
from . import views
from .views import PatientRecordsView, EmotionLogView, EmotionLogChartView

urlpatterns =[

    path('', views.home, name='home'),
    path('signup/', views.register_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('doctor-dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('patient-dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('patient-records/', PatientRecordsView.as_view(), name='patient-records'),
    path('emotion-logs/', EmotionLogView.as_view(), name='emotion-logs'),
    path('emotion-log-chart/<int:days>/', EmotionLogChartView.as_view(), name='emotion-log-chart'),
]
    

 

