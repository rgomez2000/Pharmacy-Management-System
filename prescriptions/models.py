from django.db import models
from patient.models import Patient
from drugs.models import Drug
from django.contrib.auth.models import User
from django_currentuser.db.models import CurrentUserField

class Prescription(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, related_name="prescriptions")
    medication = models.ForeignKey(Drug, on_delete=models.CASCADE, null=True)
    dosage = models.CharField(max_length=100)
    instructions = models.TextField(max_length=1000)
    doctor_name = models.CharField(max_length=100)
    in_person = models.BooleanField(default=False)
    date_prescribed = models.DateTimeField(auto_now_add=True)
    is_filled = models.BooleanField(default=False)  # New field to track if prescription is filled
    picked_up = models.BooleanField(default=False)  # New field to track if prescription has been picked up by patient
    created_by = CurrentUserField()

    def __str__(self):
        return f"{self.medication.drug_name} for {self.patient.first_name}  {self.patient.last_name}"