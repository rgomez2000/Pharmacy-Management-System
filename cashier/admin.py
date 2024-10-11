from django.contrib import admin
from .models import InventoryItem, Purchase

# Register your models here.
admin.site.register(InventoryItem)
admin.site.register(Purchase)
