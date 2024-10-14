from django import forms
from .models import Drug

class DrugForm(forms.ModelForm):
    DOSAGE_FORM = [
        ("Tablet", "Tablet"),
        ("Capsule", "Capsule"),
        ("Liquid", "Liquid"),
        ("Ointment", "Ointment")
    ]

    DRUG_CLASS= [
        ('Analgesics', 'Analgesics'),
        ('Antibiotics', 'Antibiotics'),
        ('Antivirals', 'Antivirals'),
        ('Antidepressants', 'Antidepressants'),
        ('Antihypertensives', 'Antihypertensives'),
        ('Antihistamines', 'Antihistamines'),
        ('Anticoagulants', 'Anticoagulants'),
        ('Diuretics', 'Diuretics'),
        ('Hormonal agents', 'Hormonal agents'),
        ('Statins', 'Statins'),
        ('Beta-blockers', 'Beta-blockers'),
        ('Corticosteroids', 'Corticosteroids'),
        ('Mood stabilizers', 'Mood stabilizers'),
        ('Antipsychotics', 'Antipsychotics'),
        ('Immunosuppressants', 'Immunosuppressants'),
    ]

    RX_CHOICE = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]
        
    drug_name = forms.CharField(
        label='Drug Name',
        widget=forms.TextInput(attrs={
            "placeholder" : ""
        })
    )
    generic_name = forms.CharField(
        label='Generic Name',
        widget=forms.TextInput(attrs={
            "placeholder" : ""
        })
    )
    brand_name = forms.CharField(
        label='Brand Name',
        widget=forms.TextInput(attrs={
            "placeholder" : ""
        })
    )
    dosage_form = forms.ChoiceField(
        label='Dosage Form',
        choices=DOSAGE_FORM,
    )
    strength = forms.IntegerField(
        label='Strength/Unit',
        min_value=0,
    )
    manufacturer = forms.CharField(
        label='Manufacturer',
        widget=forms.TextInput(attrs={
            "placeholder" : ""
        })
    )
    drug_class = forms.ChoiceField(
        label='Classification',
        choices=DRUG_CLASS,
    )
    indications = forms.CharField(
        label='Indications',
        widget=forms.Textarea(attrs={
            "placeholder" : ""
        })
    )
    side_effects = forms.CharField(
        label='Side Effects',
        widget=forms.Textarea(attrs={
            "placeholder" : ""
        })
    )
    contraind = forms.CharField(
        label='Contraindications',
        widget=forms.Textarea(attrs={
            "placeholder" : ""
        })
    )
    dosage_inst = forms.CharField(
        label='Dosage Instructions',
        widget=forms.Textarea(attrs={
            "placeholder" : ""
        })
    )
    stock_qty = forms.IntegerField(
        label='Stock Quantity',
        min_value=0,
    )
    exp_date = forms.DateField(
        label='Expiration Date',
        widget=forms.SelectDateWidget()
    )
    rx_required = forms.ChoiceField(
        label='Prescription Requisite',
        choices=RX_CHOICE,
    )
    price = forms.DecimalField(
        label='Cost/Unit',
        min_value=0,
        decimal_places=2,
        step_size=0.01,
    )
    storage_cond = forms.CharField(
        label='Storage Conditions',
        widget=forms.Textarea(attrs={
            "placeholder" : ""
        })
    )
    bar_code = forms.CharField(
        label='UPC',
        widget=forms.TextInput(attrs={
            "placeholder" : ""
        })
    )
    class Meta:
        model = Drug
        fields = [
            "drug_name",
            "generic_name",
            "brand_name",
            "dosage_form",
            "strength",
            "manufacturer",
            "drug_class",
            "rx_required",
            "indications",
            "side_effects",
            "contraind",
            "dosage_inst",
            "storage_cond",
            "stock_qty",
            "exp_date",
            "price",
            "bar_code",
        ]
