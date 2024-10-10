from django.urls import path
from .views import drug_create_view

# URLConf
urlpatterns = [
    path('medicine/', drug_create_view, name='medicine'),
]