from django.contrib import admin
from .models import Prescription

# Register your models here.
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ("patient", "medication", "dosage", "instructions", "doctor_name", "date_prescribed")

admin.site.register(Prescription, PrescriptionAdmin)
