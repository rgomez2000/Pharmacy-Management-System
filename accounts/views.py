from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from .forms import LoginForm#, RegisterForm

from .models import UserProfile
from django.contrib.auth.models import User
from django.contrib import messages

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required


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
        print("Form Data:", request.POST)  # Debugging line
        print("Form is valid:", form.is_valid())  # Debugging line

        if form.is_valid():
            user = form.get_user()  # Get the authenticated user
            user_profile = user.userprofile
            
            # Successful login logic
            user_profile.failed_login_attempts = 0
            user_profile.save()
            login(request, user)

            # Redirect to change password if it's the first login
            if not user_profile.password_changed:
                return redirect("change_password")
            
            return redirect("landingPage")
        
        print("Form Errors:", form.errors)

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


# def login_view(request):
#     if request.method == "POST":
#         form = LoginForm(data=request.POST)
#         print("Form Data:", request.POST)  # Debugging line
#         print("Form is valid:", form.is_valid())  # Debugging line

#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')

#             # Authenticate the user
#             user = authenticate(username=username, password=password)
            
#             if user is not None:
#                 user_profile = user.userprofile
                
#                 # Check if the user account is locked
#                 if user_profile.is_locked:
#                     messages.error(request, "This account is locked. Please contact an admin.")
#                     return render(request, "login.html", {"form": form})

#                 # Successful login logic
#                 user_profile.failed_login_attempts = 0
#                 user_profile.save()
#                 login(request, user)

#                 # Redirect to change password if it's the first login
#                 if not user_profile.password_changed:
#                     return redirect("change_password")
                
#                 return redirect("landingPage")

#             # If the user is None, it means the credentials are invalid
#             messages.error(request, "Invalid username or password.")
        
#         print("Form Errors:", form.errors)

#         # Handle invalid login (failed login attempts)
#         username = form.cleaned_data.get("username")
#         if username:
#             user = User.objects.filter(username=username).first()
#             if user:
#                 user_profile = user.userprofile
#                 user_profile.failed_login_attempts += 1
                
#                 if user_profile.failed_login_attempts >= 5:
#                     user_profile.is_locked = True
#                     user_profile.save()
#                     messages.error(request, "Your account has been locked due to too many failed login attempts.")
#                 else:
#                     user_profile.save()

#     else:
#         form = LoginForm()

#     return render(request, "login.html", {"form": form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user) 
            user.userprofile.password_changed = True  # Update the first time login
            user.userprofile.save()
            messages.success(request, 'Your password was successfully updated!')
            return redirect('landingPage')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'change_password.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect("landingPage")


def lockout_view(request):
    return render(request, 'lockout.html')