from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from django.contrib.auth.models import User
from django.contrib import messages

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        validate_form = form.is_valid()
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        if validate_form:
            # If we reach here, both user and password are valid and we can login
            user = authenticate(username=username, password=password)

            if user is not None:
                user_profile = user.userprofile
                # Check during login if the `is_locked` flag is set to True. If yes, does not matter if login
                # is correct - need to stop the login process now.
                if user_profile.is_locked:
                    messages.error(request, "Your account has been locked. Please contact an admin.")
                
                # If account is not locked, reset failed_login_attempts to 0, save the profile, and
                # proceed with login.
                else:
                    user_profile.failed_login_attempts = 0
                    user_profile.save()
                    login(request, user)
                    
                    return redirect("admin:index")
                # if not user.password_changed:
                #     return redirect("change_password")
                # return redirect("landingPage") 

        else:
            # If we reach here, either the provided username and/or password are invalid.
            if username is not None:
                user = User.objects.filter(username=username).first()
                # If the username is provided, grab the associated User object from the User model
                #  - if it is not None, then the password is invalid. Get the underlying `userprofile`
                # and add a failed_login_attempt.
                if user is not None:
                    user_profile = user.userprofile
                    user_profile.failed_login_attempts += 1
                    # If the account is locked, display the locked message regardless of the count of
                    # failed_login_attempts
                    if user_profile.is_locked:
                        messages.error(request, "Your account has been locked. Please contact an admin.")
                    # Otherwise, once we reach 5 failed login attempts, send a message indicating that
                    # the account has now been locked.
                    elif user_profile.failed_login_attempts >= 5:
                        user_profile.is_locked = True
                        messages.error(request, "Your account has been locked due to too many failed login attempts.")
                    # Otherwise display a general invalid message (this can occur up to 4 times.)
                    else:
                        messages.error(request, "Invalid username or password.")
                    # Save the user profile so that the failed_login_attempts and/or is_locked values
                    # are stored.
                    user_profile.save()
                
                # If we reach this `else`, then the username was invalid - just display a generic message
                else:
                    messages.error(request, "Invalid username or password.")          
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})

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