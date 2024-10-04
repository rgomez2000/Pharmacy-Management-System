from django.urls import path
from .views import about_view

# URLConf
urlpatterns = [
    path('about/', about_view, name='about'),
]