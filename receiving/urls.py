from django.urls import path
from . import views

urlpatterns = [
    path('', views.receiving_main, name='receiving_main'),
    path('receive/<int:pk>/', views.receive_order, name='receive_order')
]