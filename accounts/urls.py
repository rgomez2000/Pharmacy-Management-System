from django.urls import path

from .views import login_view, logout_view, lockout_view, change_password

urlpatterns = [
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path('lockout/', lockout_view, name='lockout'),
    path('change_password/', change_password, name='change_password'),
]
