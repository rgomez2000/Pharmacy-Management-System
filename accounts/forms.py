from django import forms
from django.contrib.auth.forms import AuthenticationForm#, UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import UserProfile

# class RegisterForm(UserCreationForm):
#     email = forms.EmailField(
#         max_length=254, help_text="Required. Please enter a valid email address."
#     )

#     class Meta(UserCreationForm.Meta):
#         model = User
#         fields = UserCreationForm.Meta.fields + ("email",)


# using the AuthenticationForm class from django
class LoginForm(AuthenticationForm):
    def clean(self):
        super().clean()
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError("Invalid username or password.")
            
            try:
                user_profile = user.userprofile
            except UserProfile.DoesNotExist:
                raise forms.ValidationError("User profile does not exist.")
            # try:
            #     user = User.objects.get(username=username)
            # user_profile = user.userprofile
            
            # Check if the user account is locked
            if user_profile.is_locked:
                raise forms.ValidationError("This account is locked. Please contact an admin.")
            
            # Check if this is the first login
            if not user_profile.password_changed:
                self.first_login = True

                    
            # except User.DoesNotExist:
            #     raise forms.ValidationError("This username does not exist.")

        return self.cleaned_data
