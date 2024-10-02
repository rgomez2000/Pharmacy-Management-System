from django.shortcuts import render
from .models import Prescription

def all(request):
    my_prescriptions = Prescription.objects.all().values()
    context = {
        "my_prescriptions" : my_prescriptions
    }
    return render(request, "all_prescriptions.html", context)

def details(request, id):
    my_prescription = Prescription.objects.get(id=id)
    context = {
        "prescription" : my_prescription
    }
    return render(request, "details.html", context)

def prescriptions_main(request):
    return render(request, 'main.html')

def add(request):
    return render(request, 'add.html')
