from django.contrib import admin
from .models import InventoryItem, Purchase, PurchasedItemDetails, Receipt

# Register your models here.
class PurchaseInline(admin.TabularInline):
    model = PurchasedItemDetails
    extra = 1

class PurchaseAdmin(admin.ModelAdmin):
    inlines = (PurchaseInline,)

class InventoryItemAdmin(admin.ModelAdmin):
    inlines = (PurchaseInline,)

admin.site.register(InventoryItem, InventoryItemAdmin)
admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(Receipt)
