from django.db import models
from prescriptions.models import Prescription

class PrescriptionLog(models.Model):
    pharmacist_name = models.CharField(max_length=100)
    prescription_number = models.CharField(max_length=50)
    patient_name = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    drug_type = models.CharField(max_length=100,blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"Log for {self.patient_name} - {self.prescription_number}"