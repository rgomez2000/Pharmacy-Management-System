from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect, render, get_object_or_404
from .forms import PrescriptionForm
from .models import Prescription

def is_pharmacist(user):
    return user.groups.filter(name='Pharmacist').exists()

def is_pharmacy_manager(user):
    return user.groups.filter(name='Pharmacy Manager').exists()

def is_pharmacy_technician(user):
    return user.groups.filter(name='Pharmacy Technician').exists()

@login_required
@user_passes_test(is_pharmacist)
def add_prescription(request):
    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('prescriptions')
    else:
        form = PrescriptionForm()  # Makes sure the form is being created

    return render(
        request, 'add_prescription.html', {'form': form}
    )  # Makes sure the form is passed to the template

@login_required
@user_passes_test(is_pharmacist or is_pharmacy_manager or is_pharmacy_technician)
def prescriptions_main(request):
    return render(request, 'main.html')

@login_required
@user_passes_test(is_pharmacist or is_pharmacy_manager or is_pharmacy_technician)
def prescription_list(request):
    prescriptions = Prescription.objects.all()  # Retrieves all of the prescriptions
    return render(request, 'prescription_list.html', {'prescriptions': prescriptions})

@login_required
@user_passes_test(is_pharmacist)
def delete_prescription(request, pk):
    # Get the prescription by primary key (pk)
    prescription = get_object_or_404(Prescription, pk=pk)

    if request.method == 'POST':
        if 'delete' in request.POST:
            prescription.delete()
            return redirect('prescription_list')
        else:
            return redirect('prescription_list') 
    
    return render(request, 'confirm_delete.html', {'prescription': prescription})

@login_required
@user_passes_test(is_pharmacist)
def edit_prescription(request, pk):
    prescription = get_object_or_404(Prescription, pk=pk)

    if request.method == 'POST':
        form = PrescriptionForm(request.POST, instance=prescription)  # Pass the instance to update
        if form.is_valid():
            if 'save' in request.POST:
                form.save()
                return redirect('prescription_list')  # Redirect to the prescription list after saving
            else:
                return redirect('prescription_list') # Redirect to the prescription list after canceling without saving changes
    else:
        form = PrescriptionForm(instance=prescription)  # Populate the form with existing data

    return render(request, 'edit_prescription.html', {'form': form, 'prescription': prescription})

@login_required
@user_passes_test(is_pharmacist)
def fill_prescription(request, pk):
    prescription = get_object_or_404(Prescription, pk=pk)

    if request.method == 'POST':
        form = PrescriptionForm(request.POST, instance=prescription)
        if form.is_valid():
            # Mark as filled
            prescription.is_filled = True
            form.save()
            return redirect('prescription_list')  # Redirect to list view after filling

    else:
        form = PrescriptionForm(instance=prescription)  # Populate with existing data

    return render(request, 'fill_prescription.html', {'form': form, 'prescription': prescription})