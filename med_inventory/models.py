from django.db import models

class Medication(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    @property
    def availability_status(self):
        if self.quantity > 10:
            return 'In Stock'
        elif self.quantity > 0:
            return 'Low Stock'
        else:
            return 'Out of Stock'
        
    class Meta:
        permissions = [
            ("can_check_inventory", "Can check inventory"),
        ]
