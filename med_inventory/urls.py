from django.urls import path
from . import views

urlpatterns = [
    path('inventory-check/', views.inventory_check, name='inventory_check'),
]