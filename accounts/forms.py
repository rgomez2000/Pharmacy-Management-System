from django import forms
from django.contrib.auth.forms import AuthenticationForm#, UserCreationForm
from django.contrib.auth.models import User


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
        
        if username:
            try:
                user = User.objects.get(username=username)
                user_profile = user.userprofile
                
                if user_profile.is_locked:
                    raise forms.ValidationError("This account is locked. Please contact an admin.")
                    
            except User.DoesNotExist:
                pass  # If user doesn't exist, just continue

        return self.cleaned_data
