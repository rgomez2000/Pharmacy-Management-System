from django.urls import path
from . import views

urlpatterns = [
    path("", views.prescriptions_main, name="prescriptions"),
    path("add-prescription/", views.add_prescription, name="add_prescription"),
    path('prescriptions/', views.prescription_list, name='prescription_list'),
    path('prescriptions/delete/<int:pk>/', views.delete_prescription, name='delete_prescription'), 
    path('prescriptions/edit/<int:pk>/', views.edit_prescription, name='edit_prescription'),  
]