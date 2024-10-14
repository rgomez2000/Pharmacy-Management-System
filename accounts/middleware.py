from django.utils import timezone
from django.shortcuts import redirect
from .models import UserProfile  # Import your UserProfile model
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from django.core.exceptions import PermissionDenied

class LockoutMiddleware:
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the user is logged in
        if request.user.is_authenticated:
            # If authenticated, allow the request to continue
            return self.get_response(request)

        # If user is not authenticated and accessing the login view
        if request.path == '/login/':  # Update the path as needed
            username = request.POST.get('username', None)
            if username:
                try:
                    user_profile = UserProfile.objects.get(user__username=username)

                    # Check lockout conditions
                    if user_profile.lockout_time and timezone.now() < user_profile.lockout_time:
                        # Redirect to a lockout page or display a message
                        return redirect('lockout_page')  # Replace with your lockout page URL

                except UserProfile.DoesNotExist:
                    # If the user doesn't exist, just continue
                    pass

        # Continue processing the request
        response = self.get_response(request)
        return response

class LoginAttemptMiddleware:
    # MAX_ATTEMPTS = 5
    # LOCKOUT_DURATION = 10  # Lockout duration in seconds

    # def __init__(self, get_response):
    #     self.get_response = get_response

    # def __call__(self, request):
    #     if request.method == "POST" and request.path == "/accounts/login/":
    #         username = request.POST.get("username")
    #         if username:
    #             user = User.objects.filter(username=username).first()
    #             if user:
    #                 now = timezone.now()
    #                 # Check the user's profile for login attempts and lockout time
    #                 profile = user.userprofile
    #                 if profile.login_attempts >= self.MAX_ATTEMPTS:
    #                     if now < profile.lockout_until:
    #                         raise PermissionDenied("Account is locked. Please try again later.")
    #                     else:
    #                         profile.login_attempts = 0  # Reset attempts after lockout period

    #                 # Update the user profile if login fails
    #                 if request.POST.get("password") and not authenticate(username=username, password=request.POST.get("password")):
    #                     profile.login_attempts += 1
    #                     profile.save()

        # return self.get_response(request)
        pass