from django.urls import path
from . import views

urlpatterns = [
    path('inventory-check/', views.inventory_check, name='inventory_check'),
    path('order-medication/', views.order_medication, name='order_medication'),
    path('manager-dash/', views.manager_dash, name='manager_dash'),
    path('remove_expired_drug/<int:drug_id>/', views.remove_expired_drug, name='remove_expired_drug'),
]