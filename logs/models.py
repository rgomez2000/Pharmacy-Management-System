from django.db import models
from patient.models import Patient
from accounts.models import UserProfile
from cashier.models import InventoryItem
from drugs.models import Drug 
from django_currentuser.db.models import CurrentUserField
from django.contrib.auth.models import User

class PrescriptionLog(models.Model):
    pharmacist_name = CurrentUserField()
    prescription_number = models.CharField(max_length=50)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    drug_type = models.CharField(max_length=100,blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"Log for {self.patient} - {self.prescription_number}"
    

class DrugDeletionLog(models.Model):
    EVENT_TYPES = [
        ('deleted', "Drug Deleted"),
    ]
    deleted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    drug_name = models.CharField(max_length=50)
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Deletion log for {self.drug_name} - {self.timestamp}"
    
class AccountActivityLog(models.Model):
        EVENT_TYPES = [
        ('login', "login"),
        ('logout', "logout"),
        ('failed', "failed"),
        ('locked', "locked"),
        ('unlocked', "unlocked")
        ]
        user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
        event_type = models.CharField(max_length=10, choices=EVENT_TYPES)
        date = models.DateField(auto_now_add=True)
        time = models.TimeField(auto_now_add=True)
        ip_address = models.GenericIPAddressField(null=True, blank=True)
        failed_login = models.CharField(max_length=42,null=True, blank=True)

        def __str__(self):
            return f"{self.event_type} event for {self.user} at {self.date}, {self.time}"
        
class InventoryLog(models.Model):
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    user = CurrentUserField()
    old_quantity = models.PositiveIntegerField()
    new_quantity = models.PositiveIntegerField()
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)  
    change_reason = models.CharField(max_length=42,null=True, blank=True)

    def __str__(self):
        return f"Change log for {self.item.name} on {self.date}, {self.date}"
    
class DrugLog(models.Model):
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE)
    user = CurrentUserField()
    old_quantity = models.PositiveIntegerField()
    new_quantity = models.PositiveIntegerField()
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    change_reason = models.CharField(max_length=42,null=True, blank=True)

    def __str__(self):
        return f"Change log for {self.drug.drug_name} on {self.date}, {self.time}"