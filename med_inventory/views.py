from django.shortcuts import render
from .models import Medication
from .forms import MedicationSearchForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

@login_required
def check_medication_availability(request):
    if not request.user.has_perm('inventory.can_check_inventory'):
        raise PermissionDenied
    
    form = MedicationSearchForm()
    results = None

    if request.method == 'POST':
        form = MedicationSearchForm(request.POST)
        if form.is_valid():
            medication_name = form.cleaned_data['name']
            results = Medication.objects.filter(name__icontains=medication_name)

    return render(request, 'inventory/check_med.html', {'form': form, 'results': results})