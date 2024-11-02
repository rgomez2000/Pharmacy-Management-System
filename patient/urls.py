from django.urls import path
from . import views

urlpatterns = [
    path('patients/', views.patients_main, name='patients_main'),
    path('patient_list/', views.patient_list, name='patient_list'),
    path("add-patient/", views.add_patient, name="add_patient"),
    path('delete/<int:pk>/', views.delete_patient, name='delete_patient'),
    path('edit/<int:pk>/', views.edit_patient, name='edit_patient'),
    path('details/<int:pk>/', views.patient_details, name='patient_details')
]