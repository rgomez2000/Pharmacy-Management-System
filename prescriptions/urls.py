from django.urls import path
from . import views

urlpatterns = [
    path("", views.prescriptions_main, name="prescriptions"),
    path("add-prescription/", views.add_prescription, name="add_prescription"),
    path('prescriptions/', views.prescription_list, name='prescription_list'),
]