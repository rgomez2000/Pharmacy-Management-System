from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProfile
from django.contrib.auth.models import User


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    This method is called when the post_save signal is sent by the save_model function
    in the admin view. This function first creates a user profile if one is needed, then
    resets the user  failed_login_attempts to 0 any time this user is changed and the
    value of `is_locked` is False.
    """
    if not hasattr(instance, "userprofile"):
        # Create the userprofile if one has not been created
        UserProfile.objects.create(user=instance)
        instance.userprofile.password_changed = False

    if not instance.userprofile.is_locked:
        # If the account is unlocked, reset failed_login_attempts to 0
        instance.userprofile.failed_login_attempts = 0
    
    # Save the changes to the userprofile model
    instance.userprofile.save()
