from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import DrugForm

# Custom decorator to check if the user is in allowed groups
def allowed_groups(*groups):
    def in_groups(user):
            return user.groups.filter(name__in=groups).exists()
    return user_passes_test(in_groups)

@login_required
@allowed_groups('Pharmacist', 'Pharmacy Manager', 'Pharmacy Technician')
def drug_create_view(request):
    if request.method == 'POST':
        form = DrugForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('drug_success')
    else:
        form = DrugForm()

    context = {
        'form': form,
    }
    return render(request, "drug_form.html", context)

@login_required
@allowed_groups('Pharmacist', 'Pharmacy Manager', 'Pharmacy Technician')
def drug_success_view(request):
    return render(request, 'drug_success.html')