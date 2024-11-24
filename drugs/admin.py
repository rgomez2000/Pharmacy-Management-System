from django.contrib import admin
from .models import Drug


class DrugAdmin(admin.ModelAdmin):
    list_display = ('id', 'drug_name', 'generic_name', 'brand_name', 'drug_class', 'dosage_form', 'strength', 'exp_date')

admin.site.register(Drug, DrugAdmin)