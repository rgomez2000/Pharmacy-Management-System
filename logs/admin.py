from django.contrib import admin
from .models import PrescriptionLog
from .models import DrugDeletionLog
from .models import AccountActivityLog
from .models import InventoryLog
from .models import DrugLog

class PrescriptionLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'pharmacist_name', 'prescription_number', 'patient', 'date', 'time', 'drug_type', 'quantity')

class AccountActivityLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'event_type', 'date', 'time', 'ip_address', 'failed_login')

class InventoryLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'item', 'old_quantity', 'new_quantity', 'date', 'time','change_reason')

class DrugLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'drug', 'old_quantity', 'new_quantity', 'date', 'time','change_reason')

admin.site.register(PrescriptionLog, PrescriptionLogAdmin)
admin.site.register(AccountActivityLog, AccountActivityLogAdmin)
admin.site.register(InventoryLog, InventoryLogAdmin)
admin.site.register(DrugLog, DrugLogAdmin)
admin.site.register(DrugDeletionLog)