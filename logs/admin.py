from django.contrib import admin
from .models import PrescriptionLog

class PrescriptionLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'pharmacist_name', 'prescription_number', 'patient_name', 'date', 'time', 'drug_type', 'quantity')

admin.site.register(PrescriptionLog, PrescriptionLogAdmin)
