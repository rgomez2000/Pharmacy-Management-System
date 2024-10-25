from django.urls import path
from .views import check_medication_availability

urlpatterns = [
    path('check-med/', check_medication_availability, name='check_med'),
]