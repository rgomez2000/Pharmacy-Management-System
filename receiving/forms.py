from django import forms
from med_inventory.models import Order
from django.utils.safestring import SafeString

class OrderForm(forms.ModelForm):
    class Meta:
        # allows styling to be used on the form using the "form-group" classed div
        def as_div(self):
            return SafeString(super().as_div().replace("<div>", "<div class='form-group'>"))

        model = Order
        fields = ['drug', 'quantity']
    
    def __init__(self, *args, **kwargs):
        # Overwrite the standard __init__ method to make the "drug" and
        # "quantity" fields read-only
        super().__init__(*args, **kwargs)
        self.fields['drug'].disabled = True
        self.fields['quantity'].disabled = True
