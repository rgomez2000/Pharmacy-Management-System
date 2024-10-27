from django.shortcuts import render, get_object_or_404
from .models import Stock
from .decorators import pharmacist_required
from drugs.models import Drug

@pharmacist_required
def inventory_check(request):
    drugs = Drug.objects.all()  # Fetch all drugs
    selected_drug = None
    stock_qty = None
    stock_status = None

    if request.method == 'GET' and 'drug' in request.GET:
        selected_drug_id = request.GET['drug']
        selected_drug = get_object_or_404(Drug, id=selected_drug_id)

        # Fetch stock information for the selected drug
        stock = Stock.objects.filter(drug=selected_drug).first()  # Get the first stock entry for the selected drug

        if stock:
            stock_qty = stock.stock_qty  
            stock_status = stock.stock_status()
        else:
            stock_qty = 0  # Default to 0 if no stock entry exists
            stock_status = "No stock entry found."

    return render(request, 'inventory_check.html', {
        'drugs': drugs,
        'selected_drug': selected_drug,
        'stock_qty': stock_qty,
        'stock_status': stock_status,
    })