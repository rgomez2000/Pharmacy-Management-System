from django import forms

class MedicationSearchForm(forms.Form):
    name = forms.CharField(label='Medication Name', max_length=255)