from django.urls import path
from . import views

urlpatterns = [
    path("", views.prescriptions_main, name="prescriptions"),
    path("add-prescription/", views.add_prescription, name="add_prescription"),
    path('prescriptions/', views.prescription_list, name='prescription_list'),
    path('prescriptions/fill/<int:pk>/', views.fill_prescription, name='fill_prescription'),
    path('prescriptions/pickup/<int:pk>/', views.pickup_prescription, name='pickup_prescription'),
    path('prescriptions/delete/<int:pk>/', views.delete_prescription, name='delete_prescription'), 
    path('prescriptions/edit/<int:pk>/', views.edit_prescription, name='edit_prescription'),  
]