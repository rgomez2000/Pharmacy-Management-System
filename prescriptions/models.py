from django.db import models

class Prescription(models.Model):
    name = models.CharField(max_length=255)
    expiry = models.DateField()

    def __str__(self):
        return f"{self.name}"