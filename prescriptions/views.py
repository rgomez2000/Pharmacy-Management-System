from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .forms import PrescriptionForm
from .models import Prescription

@login_required
def add_prescription(request):
    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('prescriptions')
    else:
        form = PrescriptionForm()  # Ensure the form is being created

    return render(
        request, 'add_prescription.html', {'form': form}
    )  # Ensure the form is passed to the template

def prescriptions_main(request):
    return render(request, 'main.html')

def prescription_list(request):
    prescriptions = Prescription.objects.all()  # Retrieve all prescriptions
    return render(request, 'prescription_list.html', {'prescriptions': prescriptions})
