from django.db import models
from patient.models import Patient
from django_currentuser.db.models import CurrentUserField

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