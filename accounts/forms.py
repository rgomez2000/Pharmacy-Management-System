from django import forms
from django.contrib.auth.forms import AuthenticationForm#, UserCreationForm
#from django.contrib.auth.models import User


# class RegisterForm(UserCreationForm):
#     email = forms.EmailField(
#         max_length=254, help_text="Required. Please enter a valid email address."
#     )

#     class Meta(UserCreationForm.Meta):
#         model = User
#         fields = UserCreationForm.Meta.fields + ("email",)


# using the AuthenticationForm class from django
class LoginForm(AuthenticationForm):
    pass
