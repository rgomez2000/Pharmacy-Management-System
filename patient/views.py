from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import ListView
from django.db.models import Q
from .models import Patient
from .forms import PatientForm

# Create your views here.
def allowed_groups(*groups):
    def in_groups(user):
            return user.groups.filter(name__in=groups).exists()
    return user_passes_test(in_groups)

@login_required
#@allowed_groups('Pharmacist', 'Pharmacy Manager', 'Pharmacy Technician')
def patients_main(request):
    return render(request, 'patients_main.html')

@login_required
#@allowed_groups('Pharmacist', 'Pharmacy Manager', 'Pharmacy Technician')
def patient_list(request):
    patients = Patient.objects.all()  # Retrieves all of the patients
    return render(request, 'patient_list.html', {'patients': patients})

@login_required
#@allowed_groups('Pharmacist', 'Pharmacy Manager', 'Pharmacy Technician')
def patient_details(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    return render(request, 'patient_details.html', {'patient' : patient})

@login_required
#@allowed_groups('Pharmacist')
def add_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('patient_list')
    else:
        form = PatientForm()  # Makes sure the form is being created

    return render(
        request, 'add_patient.html', {'form': form}
    )  # Makes sure the form is passed to the template

@login_required
@allowed_groups('Pharmacist', 'Pharmacy Manager')
def delete_patient(request, pk):
    # Get the prescription by primary key (pk)
    patient = get_object_or_404(Patient, pk=pk)

    if request.method == 'POST':
        if 'delete' in request.POST:
            patient.delete()
            return redirect('patient_list')
        else:
            return redirect('patient_list') 
    
    return render(request, 'confirm_delete_patient.html', {'patient': patient})

@login_required
#@allowed_groups('Pharmacist')
def edit_patient(request, pk):
    patient = get_object_or_404(Patient, pk=pk)

    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)  # Pass the instance to update
        if form.is_valid():
            if 'save' in request.POST:
                form.save()
                return redirect('patient_list')  # Redirect to the patient list after saving
            else:
                return redirect('patient_list') # Redirect to the patient list after canceling without saving changes
    else:
        form = PatientForm(instance=patient)  # Populate the form with existing data

    return render(request, 'edit_patient.html', {'form': form, 'patient': patient})

class SearchPatientsView(ListView):
    model = Patient
    template_name = "patient_search_results.html"
    def get_queryset(self):
        query = self.request.GET.get("query")
        return Patient.objects.filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(dob__icontains=query))
