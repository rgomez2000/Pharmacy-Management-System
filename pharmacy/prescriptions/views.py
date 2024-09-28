from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Prescription

def all(request):
    my_prescriptions = Prescription.objects.all().values()
    template = loader.get_template('all_prescriptions.html')
    context = {
        "my_prescriptions" : my_prescriptions
    }
    return HttpResponse(template.render(context, request))

def details(request, id):
    my_prescription = Prescription.objects.get(id=id)
    template = loader.get_template('details.html')
    context = {
        "prescription" : my_prescription
    }
    return HttpResponse(template.render(context, request))

def prescriptions_main(request):
    template = loader.get_template('main.html')
    return HttpResponse(template.render())
