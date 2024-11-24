from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from prescriptions.models import Prescription
from .models import PrescriptionLog, AccountActivityLog, InventoryLog, DrugLog
from accounts.models import UserProfile
from cashier.models import InventoryItem
from drugs.models import Drug
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed



@receiver(post_save, sender=Prescription)
def log_creation(sender, instance, created, **kwargs):
    if instance.is_filled:
        now = timezone.now()
        PrescriptionLog.objects.create(
            pharmacist_name = instance.created_by,
            prescription_number = instance.id,
            patient = instance.patient,
            date = now.date(),
            time = now.time(),
            drug_type = instance.medication.drug_class,
            quantity = instance.dosage
        )

# Log the user login event
@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    now = timezone.now()
    AccountActivityLog.objects.create(
        user = user,
        event_type = 'login',
        date = now.date(),
        time = now.time(),
        ip_address=request.META.get('REMOTE_ADDR')  # Capture IP address
    )

# Log the user logout event
@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    now = timezone.now()
    AccountActivityLog.objects.create(
        user = user,
        event_type = 'logout',
        date = now.date(),
        time = now.time(),
        ip_address=request.META.get('REMOTE_ADDR')  # Capture IP address
    )

# Log failed login event
@receiver(user_login_failed)
def log_user_failed(sender, credentials, request, **kwargs):
    username = credentials.get('username') # Get the UserProfile instance
    user_profile = UserProfile.objects.get(user__username=username) # Get the username
    user = user_profile.user # This is similar to instance.user

    failed_login_attempts = user_profile.failed_login_attempts
    now = timezone.now()
    AccountActivityLog.objects.create(
        user = user,
        event_type = 'failed',
        date = now.date(),
        time = now.time(),
        ip_address=request.META.get('REMOTE_ADDR'),  # Capture IP address
        failed_login = f"Attempts: {failed_login_attempts+1}"
    )

# Log account lock event
@receiver(post_save, sender=UserProfile)
def log_account_lock(sender, instance, created, **kwargs):
    # Only log when the account is locked and it's not a new user being created
    if not created and instance.is_locked:
        now = timezone.now()
        AccountActivityLog.objects.create(
            user=instance.user,
            event_type='locked',
            date=now.date(),
            time=now.time(),
            ip_address=None,
            failed_login="Account locked"
        )

# Log account unlock event
@receiver(pre_save, sender=UserProfile)
def log_account_unlock(sender, instance, **kwargs):
    if instance.pk:# Only check for changes if the item already exists
        # Get the previous value of `is_locked`
        previous_is_locked = UserProfile.objects.get(pk=instance.pk).is_locked
        
        # If the account was previously locked and is now unlocked, log the event
        if previous_is_locked and not instance.is_locked:
            now = timezone.now()
            AccountActivityLog.objects.create(
                user=instance.user,
                event_type='unlocked',
                date=now.date(),
                time=now.time(),
                ip_address=None,  
                failed_login="Account unlocked"
            )

# Log new inventory items
@receiver(post_save, sender=InventoryItem)
def log_new_inventory(sender, instance, created, **kwargs):
    now = timezone.now()
    if created:  # Only log for new items
        InventoryLog.objects.create(
            item=instance,
            old_quantity=0,  # No old quantity for new items
            new_quantity=instance.quantity,
            date=now.date(),
            time=now.time(),
            change_reason="New item added"
        )

# Log inventory changes
@receiver(pre_save, sender=InventoryItem)
def log_inventory_change(sender, instance, **kwargs):
    if instance.pk:  # Only check for changes if the item already exists
        try:
            old_instance = InventoryItem.objects.get(pk=instance.pk)
            if old_instance.quantity != instance.quantity:  # Check if quantity has changed
                now = timezone.now()
                InventoryLog.objects.create(
                    item=instance,
                    old_quantity=old_instance.quantity,
                    new_quantity=instance.quantity,
                    date=now.date(),
                    time=now.time(),
                    change_reason="Quantity updated"
                )
        except InventoryItem.DoesNotExist:
            pass  # Ignore if the item does not exist (this shouldn't happen)

# Log new drug creation
@receiver(post_save, sender=Drug)
def log_new_drug(sender, instance, created, **kwargs):
    now = timezone.now()
    if created:  # Only log for new drugs
        DrugLog.objects.create(
            drug=instance,
            old_quantity=0,  # No old quantity for new drugs
            new_quantity=instance.stock_qty,
            date=now.date(),
            time=now.time(),
            change_reason="New drug added"
        )

# Log drug changes
@receiver(pre_save, sender=Drug)
def log_drug_change(sender, instance, **kwargs):
    if instance.pk:  # Only check for changes if the drug already exists
        try:
            old_instance = Drug.objects.get(pk=instance.pk)
            if old_instance.stock_qty != instance.stock_qty:  # Check if stock quantity has changed
                now = timezone.now()
                DrugLog.objects.create(
                    drug=instance,
                    old_quantity=old_instance.stock_qty,
                    new_quantity=instance.stock_qty,
                    date=now.date(),
                    time=now.time(),
                    change_reason="Quantity updated"
                )
        except Drug.DoesNotExist:
            pass  # Ignore if the drug does not exist (this shouldn't happen)