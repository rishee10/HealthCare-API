# healthcare/urls.py
from django.urls import path
from .views import RegisterView, LoginView, PatientView, PatientDetailView, DoctorView, DoctorDetailView, PatientDoctorMappingView, PatientDoctorMappingDetailView, PatientDoctorMappingsView

urlpatterns = [
    path('api/auth/register/', RegisterView.as_view()),
    path('api/auth/login/', LoginView.as_view()),
    path('api/patients/', PatientView.as_view()),
    path('api/patients/<int:pk>/', PatientDetailView.as_view()),
    path('api/doctors/', DoctorView.as_view()),
    path('api/doctors/<int:pk>/', DoctorDetailView.as_view()),
    path('api/mappings/', PatientDoctorMappingView.as_view()),
    path('api/mappings/<int:pk>/', PatientDoctorMappingDetailView.as_view()),
    path('api/mappings/patient/<int:patient_id>/', PatientDoctorMappingsView.as_view()),
]
