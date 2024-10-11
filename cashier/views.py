# pharmacy/views.py
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from .models import Purchase, InventoryItem, Patient
from .forms import PurchaseForm

# Custom decorator to restrict views to cashiers only
def is_cashier(user):
    return user.groups.filter(name='Cashiers').exists()

@login_required
@user_passes_test(is_cashier)
def process_purchase(request):
    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            purchase = form.save(commit=False)
            # Calculate total cost
            purchase.total_cost = purchase.quantity * purchase.item.price
            purchase.save()
            return redirect('purchase_success')
    else:
        form = PurchaseForm()
    return render(request, 'pharmacy/process_purchase.html', {'form': form})

@login_required
@user_passes_test(is_cashier)
def purchase_success(request):
    return render(request, 'pharmacy/purchase_success.html')

