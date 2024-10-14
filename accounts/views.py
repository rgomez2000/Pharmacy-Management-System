from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from .forms import LoginForm#, RegisterForm

from .models import UserProfile
from django.contrib.auth.models import User
from django.utils import timezone
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
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            # user = authenticate(username=username, password=password)

            try:
                user = User.objects.get(username=username)
                profile = user.userprofile

                # Check for lockout
                if profile.lockout_time and timezone.now() < profile.lockout_time:
                    messages.error(request, "Your account is locked. Please try again later.")
                    return render(request, "login.html", {"form": form})

            except User.DoesNotExist:
                messages.error(request, "Invalid username or password.")
                return render(request, "login.html", {"form": form})
            


            if user is not None:
                # Reset failed attempts on successful login
                profile.failed_attempts = 0
                profile.lockout_time = None
                profile.save()
                login(request, user)
                messages.success(request, "Logged in successfully!")
                return redirect("landingPage")  # Redirect to a success page.
            else:
                 # Increment failed attempts
                profile.failed_attempts += 1

                if profile.failed_attempts >= 5:
                    profile.lockout_time = timezone.now() + timezone.timedelta(minutes=.5)  # Lockout for 15 minutes
                    messages.error(request, "Too many failed attempts. Your account is locked for 15 minutes.")
                else:
                    messages.error(request, "Invalid username or password.")

                profile.save()
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("landingPage")


def lockout_view(request):
    return render(request, 'lockout.html')