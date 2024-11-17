from django.urls import path
from . import views

urlpatterns = [
    path('transaction/<int:pk>/', views.transaction, name='transaction'),
    path('transaction/', views.transaction, name='transaction'),
    path('prescription_transaction/<int:pk>/', views.prescription_transaction, name='prescription_transaction'),
    path('prescription_transaction/', views.prescription_transaction, name='prescription_transaction'),
    path('select_patient/<int:pk>/', views.select_patient, name='select_patient'),
    path('select_patient/', views.select_patient, name='select_patient'),
    path('checkout/<int:pk>/', views.checkout, name='checkout'),
    path('checkout_complete/', views.checkout_complete, name='checkout_complete'),
    path('point_of_sale/', views.point_of_sale, name='point_of_sale'),
]