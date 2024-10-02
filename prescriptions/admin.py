from django.contrib import admin
from .models import Prescription

# Register your models here.
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ("name", "expiry")

admin.site.register(Prescription, PrescriptionAdmin)