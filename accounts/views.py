from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from .forms import LoginForm#, RegisterForm

from .models import UserProfile
from django.contrib.auth.models import User
from django.contrib import messages


# def register_view(request):
#     if request.method == "POST":
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             user.refresh_from_db()  # Load the profile instance created by the signal
#             user.save()
#             raw_password = form.cleaned_data.get("password1")
#             user = authenticate(username=user.username, password=raw_password)
#             login(request, user)
#             return redirect("landingPage")  # Redirect to a success page.
#     else:
#         form = RegisterForm()
#     return render(request, "register.html", {"form": form})



def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()  # Get the authenticated user
            user_profile = user.userprofile
            
            # Successful login logic
            user_profile.failed_login_attempts = 0
            user_profile.save()
            login(request, user)
            return redirect("landingPage")

        # Handle invalid login (failed login attempts)
        username = form.cleaned_data.get("username")
        if username:
            user = User.objects.filter(username=username).first()
            if user:
                user_profile = user.userprofile
                user_profile.failed_login_attempts += 1
                
                if user_profile.failed_login_attempts >= 5:
                    user_profile.is_locked = True
                    user_profile.save()
                    messages.error(request, "Your account has been locked due to too many failed login attempts.")
                else:
                    messages.error(request, "Invalid username or password")
                user_profile.save()

    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("landingPage")


def lockout_view(request):
    return render(request, 'lockout.html')