from django.db import models
from drugs.models import Drug


class Meta:
        permissions = [
            ("can_check_inventory", "Can check inventory"),
        ]

class Order(models.Model):
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    order_date = models.DateTimeField(auto_now_add=True)
    fulfilled = models.BooleanField(default=False)

    def __str__(self):
        return f"Order of {self.quantity} units for {self.drug.drug_name} on {self.order_date}"

class Notification(models.Model):
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE)
    stock_level = models.PositiveIntegerField()
    urgency = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Low Stock Alert for {self.drug.drug_name}: {self.stock_level} units left"