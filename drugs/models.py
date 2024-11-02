from django.db import models

# Create your models here.
class Drug(models.Model):
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

    drug_name    = models.CharField(max_length=255) # Common name.
    generic_name = models.CharField(max_length=255, blank=True, null=True) # Generic name.
    brand_name   = models.CharField(max_length=255, blank=True, null=True) # Brand names associated.
    dosage_form  = models.CharField(max_length=20, choices=DOSAGE_FORM) # Dosage form: tablet, capsule, liquid, ointment.
    strength     = models.PositiveIntegerField() # Amount of active ingredients per unit in mg.
    manufacturer = models.CharField(max_length=255) # Manufacturer name.
    drug_class   = models.CharField(max_length=20, choices=DRUG_CLASS) # Classification: antibiotic, analgesic...
    indications  = models.TextField(blank=True, null=True) # Medical condition for which the drug is prescribed.
    side_effects = models.TextField(blank=True, null=True) # Common side effects.
    contraind    = models.TextField(blank=True, null=True) # Conditions that serve as reasons to not use the drug.
    dosage_inst  = models.TextField(blank=True, null=True) # Recommended dosage.
    stock_qty    = models.PositiveIntegerField(default=0) # Number of units available.
    exp_date     = models.DateField() # Expiration date.
    rx_required  = models.CharField(max_length=20, choices=RX_CHOICE) # Is a prescription is necessary.
    price        = models.DecimalField(max_digits=10, decimal_places=2) # Cost of the drug per unit.
    storage_cond = models.TextField(blank=True, null=True) # Recommended storage information: temperature, light exposure...
    bar_code     = models.CharField(max_length=100, unique=True) # Unique identifier.
    created_at   = models.DateTimeField(auto_now_add=True) # Date of entry created.
    updated_at   = models.DateTimeField(auto_now=True) # Date of entry updated.

    def __str__(self):
        return self.drug_name
    
    def stock_status(self):
        if self.stock_qty <= 0:
            return "Out of Stock"
        elif self.stock_qty < 120:
            return "Low Stock"
        else:
            return "In Stock"