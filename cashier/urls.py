from django.urls import path
from . import views

urlpatterns = [
    path('process_purchase/', views.process_purchase, name='process_purchase'),
    path('purchase_success/', views.purchase_success, name='purchase_success'),
]