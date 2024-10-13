from django.urls import path
from .views import drug_create_view, drug_success_view

# URLConf
urlpatterns = [
    path('create-drug/', drug_create_view, name='create_drug'),
    path('success/', drug_success_view, name='drug_success'),
]