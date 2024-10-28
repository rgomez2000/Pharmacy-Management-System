from django.db import models
from drugs.models import Drug

class Stock(models.Model):
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE, related_name='stocks')  # Link to the Drug model
    stock_qty = models.PositiveIntegerField(default=0)  # Number of units available

    def __str__(self):
        return f"{self.drug} - {self.stock_qty} units"

    def stock_status(self):
        print(f"Calculating stock status for drug {self.drug.drug_name} with stock_qty {self.stock_qty}")
        if self.stock_qty <= 0:
            return "Out of Stock"
        elif self.stock_qty < 10:
            return "Low Stock"
        else:
            return "In Stock"
        
    class Meta:
        permissions = [
            ("can_check_inventory", "Can check inventory"),
        ]