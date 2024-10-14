from django.urls import path

from .views import login_view, logout_view, lockout_view#, register_view

urlpatterns = [
    # path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path('lockout/', lockout_view, name='lockout_page'),
]
