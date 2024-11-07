from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from drugs.models import Drug
from django.core.cache import cache

# Custom decorator to check if the user is in allowed groups
def allowed_groups(*groups):
    def in_groups(user):
            return user.groups.filter(name__in=groups).exists()
    return user_passes_test(in_groups)

@login_required
@allowed_groups('Pharmacist', 'Pharmacy Manager')
def inventory_check(request):
    cache.clear()
    drugs = Drug.objects.all()  # Fetch all drugs
    selected_drug = None
    stock_qty = None
    stock_status = None

    if request.method == 'GET' and 'drug' in request.GET and request.GET['drug']:
        selected_drug_id = request.GET['drug']
        selected_drug = get_object_or_404(Drug, id=selected_drug_id)

        stock_qty = selected_drug.stock_qty  
        stock_status = selected_drug.stock_status()  # Correctly call the method

    return render(request, 'inventory_check.html', {
        'drugs': drugs,
        'selected_drug': selected_drug,
        'stock_qty': stock_qty,
        'stock_status': stock_status,
    })