from django.urls import path
from . import views

urlpatterns = [
    path("prescriptions/", views.prescriptions_main, name="prescriptions_main"),
    path("prescriptions/all/", views.all, name="all"),
    path("prescriptions/details/<int:id>/", views.details, name="details")
]