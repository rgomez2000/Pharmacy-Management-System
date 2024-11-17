from django import forms
from .models import Purchase, InventoryItem
from prescriptions.models import Prescription

class PurchaseForm(forms.ModelForm):
    item = forms.ModelChoiceField(queryset=InventoryItem.objects.all())
    quantity = forms.IntegerField(min_value=1, initial=1)
    class Meta:
        model = Purchase
        fields = ['item', 'quantity']

class PatientSelectForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['patient']

class PrescriptionPurchaseForm(forms.ModelForm):
    prescription = forms.ModelChoiceField(queryset=Prescription.objects.all())
    class Meta:
        model = Purchase
        fields = ['prescription']
    
    def __init__(self, *args, **kwargs):
        # Overwrite the standard __init__ method to make the
        # "prescription" field only have choices associated with
        # the previously selected patient
        super().__init__(*args, **kwargs)
        if "patient" in kwargs:
            self.fields['prescription'].queryset = Prescription.objects.filter(patient=kwargs["patient"])

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['patient', 'total_cost']

    def __init__(self, *args, **kwargs):
        # Overwrite the standard __init__ method to make the
        # "total_cost" field read-only
        super().__init__(*args, **kwargs)
        self.fields['total_cost'].disabled = True