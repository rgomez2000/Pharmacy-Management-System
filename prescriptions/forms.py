from django import forms
from .models import Prescription
from django.utils.safestring import SafeString

class PrescriptionForm(forms.ModelForm):
    class Meta:
        # allows styling to be used on the form using the "form-group" classed div
        def as_div(self):
                return SafeString(super().as_div().replace("<div>", "<div class='form-group'>"))

        model = Prescription
        fields = ['patient_name', 'medication_name', 'dosage', 'instructions', 'doctor_name']
