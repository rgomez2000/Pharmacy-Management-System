from django.db import models
from django.utils import timezone
from patient.models import Patient
from prescriptions.models import Prescription
from django.contrib.auth.models import User

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


class Receipt(models.Model):
    purchase = models.OneToOneField(Purchase, on_delete=models.CASCADE, related_name="receipt")
    pharmacy_name = models.CharField(max_length=255, default="Pharmacy Awesome")
    pharmacy_address = models.TextField(default="123 Main Street, Anytown, USA")
    pharmacy_phone = models.CharField(max_length=20, default="(123) 456-7890")
    processed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  # Staff member processing transaction
    payment_type = models.CharField(max_length=50, choices=[('credit_card', 'Credit Card'), ('debit_card', 'Debit Card'), ('cash', 'Cash')])
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    cash_given = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    change = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    transaction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Receipt #{self.id} - {self.transaction_date.strftime('%Y-%m-%d %H:%M:%S')}"