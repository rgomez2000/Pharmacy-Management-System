from django import forms
from .models import Purchase, InventoryItem
from prescriptions.models import Prescription
import datetime

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
    
    def filter_patient(self, patient):
        self.fields['prescription'].queryset = Prescription.objects.filter(is_filled=True, patient=patient, picked_up=False)

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['patient', 'total_cost']

    def __init__(self, *args, **kwargs):
        # Overwrite the standard __init__ method to make the
        # "total_cost" field read-only
        super().__init__(*args, **kwargs)
        self.fields['total_cost'].disabled = True

class PaymentForm(forms.Form):
    PAYMENT_TYPES = [
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('cash', 'Cash'),
    ]
    payment_type = forms.ChoiceField(choices=PAYMENT_TYPES, widget=forms.RadioSelect)
    card_number = forms.CharField(
        max_length=16,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Card Number'}),
    )
    card_expiry = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'MM/YY'}),
    )
    card_cvv = forms.CharField(
        max_length=3,
        required=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'CVV'}),
    )
    cash_given = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={'placeholder': 'Cash Amount'}),
    )

    def clean(self):
        cleaned_data = super().clean()
        payment_type = cleaned_data.get('payment_type')
        card_number = cleaned_data.get('card_number')
        card_expiry = cleaned_data.get('card_expiry')
        card_cvv = cleaned_data.get('card_cvv')
        cash_given = cleaned_data.get('cash_given')

        if payment_type in ['credit_card', 'debit_card']:
            if not card_number:
                self.add_error('card_number', 'Card number is required for card payments.')
            if not card_expiry:
                self.add_error('card_expiry', 'Card expiry is required for card payments.')
            if not card_cvv:
                self.add_error('card_cvv', 'Card CVV is required for card payments.')
        elif payment_type == 'cash' and not cash_given:
            self.add_error('cash_given', 'Cash amount is required for cash payments.')

        return cleaned_data