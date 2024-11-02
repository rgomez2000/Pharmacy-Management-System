from django import forms

class DrugSearchForm(forms.Form):
    name = forms.CharField(label='Drug Name', max_length=255)