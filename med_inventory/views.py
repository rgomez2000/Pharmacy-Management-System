from django.shortcuts import render, get_object_or_404
from .models import Stock
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

        #Fetch stock information for the selected drug
        stock = Stock.objects.filter(drug=selected_drug).first()  # Get the first stock entry for the selected drug

        if stock:
            stock.refresh_from_db()
            stock_qty = stock.stock_qty  
            stock_status = stock.stock_status()  # Correctly call the method
            print(f"Selected Drug: {selected_drug.drug_name}, Stock Quantity: {stock_qty}, Stock Status: {stock_status}")
        else:
            stock_qty = 0
            stock_status = "No stock entry found."
            print(f"No stock entry found for drug: {selected_drug.drug_name}")

    return render(request, 'inventory_check.html', {
        'drugs': drugs,
        'selected_drug': selected_drug,
        'stock_qty': stock_qty,
        'stock_status': stock_status,
    })
