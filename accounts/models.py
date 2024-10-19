from django.db import models
from django.contrib.auth.models import User
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    failed_login_attempts = models.IntegerField(default=0)
    is_locked = models.BooleanField(default=False)
    
    # Track wheter user has changed their password after first login
    password_requires_change = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username
    
