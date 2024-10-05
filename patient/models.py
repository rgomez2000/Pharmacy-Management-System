from django.db import models

class Patient(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    dob = models.DateField()
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    email = models.EmailField()
    insurance = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.first_name} {self.last_name} [{self.dob}]"