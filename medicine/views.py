from django.shortcuts import render
from .forms import DrugForm

def drug_create_view(request):
    form = DrugForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = DrugForm()

    context = {
        'form': form,
    }

    return render(request, "medicine_form.html", context)

