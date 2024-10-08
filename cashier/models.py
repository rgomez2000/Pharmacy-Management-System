from django.db import models
from django.utils import timezone
from patient.models import Patient


class InventoryItem(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    expiry_date = models.DateField()

class Purchase(models.Model):
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    purchase_date = models.DateTimeField(default=timezone.now)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
