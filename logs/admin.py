from django.contrib import admin
from .models import PrescriptionLog
from .models import DrugDeletionLog
class PrescriptionLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'pharmacist_name', 'prescription_number', 'patient', 'date', 'time', 'drug_type', 'quantity')

admin.site.register(PrescriptionLog, PrescriptionLogAdmin)
admin.site.register(DrugDeletionLog)