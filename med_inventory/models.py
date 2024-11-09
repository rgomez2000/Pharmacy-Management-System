from django.db import models
from drugs.models import Drug


class Meta:
        permissions = [
            ("can_check_inventory", "Can check inventory"),
        ]

class Order(models.Model):
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE)  # Link to the Drug model
    quantity = models.PositiveIntegerField()  # Quantity ordered
    order_date = models.DateTimeField(auto_now_add=True)  # Automatically set the date when the order is created

    def __str__(self):
        return f"Order of {self.quantity} units for {self.drug.drug_name} on {self.order_date}"