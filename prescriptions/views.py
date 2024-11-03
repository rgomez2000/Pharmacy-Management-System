from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from .forms import PrescriptionForm
from .models import Prescription

def allowed_groups(*groups):
    def in_groups(user):
            return user.groups.filter(name__in=groups).exists()
    return user_passes_test(in_groups)

@login_required
@allowed_groups('Pharmacist', 'Pharmacy Manager', 'Pharmacy Technician')
def prescriptions_main(request):
    return render(request, 'main.html')

@login_required
@allowed_groups('Pharmacist', 'Pharmacy Manager', 'Pharmacy Technician')
def prescription_list(request):
    prescriptions = Prescription.objects.all()  # Retrieves all of the prescriptions
    return render(request, 'prescription_list.html', {'prescriptions': prescriptions})

@login_required
@allowed_groups('Pharmacist')
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
@allowed_groups('Pharmacist')
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
@allowed_groups('Pharmacist')
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
@allowed_groups('Pharmacist')
def fill_prescription(request, pk):
    prescription = get_object_or_404(Prescription, pk=pk)

    if request.method == 'POST':
        form = PrescriptionForm(request.POST, instance=prescription)
        if form.is_valid():
            # Check to see if there is enough stock to fill the prescription
            drug = prescription.medication # Grabs the drug that is associated with the prescription being filled
            required_dosage = int(prescription.dosage) # Converts the dosage to an Int
            if drug.stock_qty >= required_dosage:
                # Will update the stock amount by deducting the stock from the prescription amount needed
                drug.stock_qty -= required_dosage
                drug.save()
                # Mark prescripton as filled
                prescription.is_filled = True
                form.save()
                messages.success(request, 'Prescription successfully filled.')
                return redirect('prescription_list')  # Redirect after filling prescription and updating medicine stock
            else:
                # Display error message if stock is insufficient
                messages.error(request, f"Not enough stock to fill this prescription. Available stock: {drug.stock_qty}.")

    else:
        form = PrescriptionForm(instance=prescription)  # Populate with existing data

    return render(request, 'fill_prescription.html', {'form': form, 'prescription': prescription})

@login_required
def pickup_prescription(request, pk):
    prescription = get_object_or_404(Prescription, pk=pk)

    if request.method == 'POST':
        form = PrescriptionForm(request.POST, instance=prescription)
        if form.is_valid():
            # Check to see if there is enough stock to fill the prescription
            drug = prescription.medication # Grabs the drug that is associated with the prescription being picked up
            drug.save()
            # Mark prescripton as filled
            prescription.picked_up = True
            form.save()
            messages.success(request, 'Prescription successfully picked up.')
        return redirect('prescription_list')
    else:
        form = PrescriptionForm(instance=prescription)  # Populate with existing data

    return render(request, 'pickup_prescription.html', {'form': form, 'prescription': prescription})