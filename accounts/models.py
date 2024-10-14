from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class UserProfile(models.Model):
    # establishes a one-to-one relationship with the django User model
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    # tracks how many times the user has failed to log in
    failed_attempts = models.PositiveIntegerField(default=0)
    # indicates until when the user is locked out
    lockout_time = models.DateTimeField(null=True, blank=True) 

    def __str__(self):
        return f"{self.user.username}'s profile"