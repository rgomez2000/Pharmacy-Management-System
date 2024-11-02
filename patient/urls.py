from django.urls import path
from . import views

urlpatterns = [
    path('patient_list/', views.patient_list, name='patient_list'),
    path("patients/add-patient/", views.add_patient, name="add_patient"),
    path('patients/delete/<int:pk>/', views.delete_patient, name='delete_patient'),
    path('patients/edit/<int:pk>/', views.edit_patient, name='edit_patient'),
    path('patients/details/<int:pk>/', views.patient_details, name='patient_details')
]