from django.contrib import admin
from med_inventory.models import Notification, Order


@admin.action(description="Mark selected orders as fulfilled")
def mark_as_fulfilled(modeladmin, request, queryset):
    queryset.update(fulfilled=True)

class OrderAdmin(admin.ModelAdmin):
    list_display = ['drug', 'quantity', 'order_date', 'fulfilled']
    actions = [mark_as_fulfilled]

admin.site.register(Order, OrderAdmin)
admin.site.register(Notification)
