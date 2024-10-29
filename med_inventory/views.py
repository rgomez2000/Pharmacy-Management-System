from django.shortcuts import render, get_object_or_404
from drugs.models import Drug
from django.core.cache import cache

def inventory_check(request):
    cache.clear()
    drugs = Drug.objects.all()  # Fetch all drugs
    selected_drug = None
    stock_qty = None
    stock_status = None


    if request.method == 'GET' and 'drug' in request.GET:
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