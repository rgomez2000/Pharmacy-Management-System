from django.db import models
from django.utils import timezone
from patient.models import Patient
from prescriptions.models import Prescription

class InventoryItem(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    expiry_date = models.DateField()

    def __str__(self):
        return self.name

class Purchase(models.Model):
    items = models.ManyToManyField(InventoryItem, through="PurchasedItemDetails")
    prescriptions = models.ManyToManyField(Prescription)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)
    purchase_date = models.DateTimeField(default=timezone.now)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_sold = models.PositiveBigIntegerField(default=1)

    def __str__(self):
        return f"Purchase on {self.purchase_date}"

class PurchasedItemDetails(models.Model):
    # "Through" class model which allows us to access details on the items contained
    # within each purchase object
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, null=True)
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(default=1)