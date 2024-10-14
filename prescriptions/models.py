from django.db import models

class Prescription(models.Model):
    patient_name = models.CharField(max_length=50)
    medication_name = models.CharField(max_length=50)
    dosage = models.CharField(max_length=100)
    instructions = models.TextField(max_length=1000)
    doctor_name = models.CharField(max_length=100)
    date_prescribed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.medication_name} for {self.patient_name}"