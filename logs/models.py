from django.db import models
from patient.models import Patient
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