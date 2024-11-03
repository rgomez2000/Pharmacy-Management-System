from django import forms
from .models import Patient
from django.utils.safestring import SafeString

class PatientForm(forms.ModelForm):
    class Meta:
        # allows styling to be used on the form using the "form-group" classed div
        def as_div(self):
            return SafeString(super().as_div().replace("<div>", "<div class='form-group'>"))

        model = Patient
        fields = ['first_name', 'last_name', 'dob', 'address', 'phone', 'email', 'insurance']
