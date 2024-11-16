from django import forms
from .models import Purchase, InventoryItem

class PurchaseForm(forms.ModelForm):
    item = forms.ModelChoiceField(queryset=InventoryItem.objects.all())
    quantity = forms.IntegerField(min_value=1, initial=1)
    class Meta:
        model = Purchase
        fields = ['item', 'quantity']

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['patient', 'total_cost']

    def __init__(self, *args, **kwargs):
        # Overwrite the standard __init__ method to make the
        # "total_cost" field read-only
        super().__init__(*args, **kwargs)
        self.fields['total_cost'].disabled = True