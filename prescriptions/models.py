from django.db import models
from patient.models import Patient
from drugs.models import Drug

class Prescription(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)
    medication = models.ForeignKey(Drug, on_delete=models.CASCADE, null=True)
    dosage = models.CharField(max_length=100)
    instructions = models.TextField(max_length=1000)
    doctor_name = models.CharField(max_length=100)
    date_prescribed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.medication.drug_name} for {self.patient.first_name}  {self.patient.last_name}"