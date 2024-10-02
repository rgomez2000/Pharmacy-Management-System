from django.urls import path
from . import views

urlpatterns = [
    path("", views.prescriptions_main, name="prescriptions"),
    path("all/", views.all, name="all"),
    path("add/", views.add, name="add"),
    path("details/<int:id>/", views.details, name="details")
]