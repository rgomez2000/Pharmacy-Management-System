from django.shortcuts import redirect, render, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from .models import Purchase, PurchasedItemDetails
from .forms import PurchaseForm, CheckoutForm

def transaction(request, pk=None):
    if pk is not None:
        purchase = get_object_or_404(Purchase, pk=pk)
    else:
        purchase = Purchase.objects.create(quantity_sold=0, total_cost=0, patient=None)
        return redirect(f'/purchasing/transaction/{purchase.id}')

    if request.method == 'POST':
        form = PurchaseForm(request.POST, instance=purchase)
        if form.is_valid():
            data = form.cleaned_data
            # Check if this item has previously been added to this purchase first
            try:
                details = PurchasedItemDetails.objects.get(item=data["item"], purchase=purchase)
                # If yes, update the quantity of that item in the purchase
                details.quantity += data["quantity"]
                details.save()
                print(details.quantity)
            except ObjectDoesNotExist:
                # if not, create an instance of the through model PurchasedItemDetails
                PurchasedItemDetails.objects.create(item=data["item"], purchase=purchase, quantity=data["quantity"])

            # Calculate and update total cost for this purchase
            purchase.total_cost += data["quantity"] * data["item"].price
            # Update the quantity of the purchase with the total quantity of items added so far
            purchase.quantity_sold += data["quantity"]
            # Save the changes
            purchase.save()
            return redirect(f'/purchasing/transaction/{purchase.id}')
    else:
        form = PurchaseForm()
    return render(request, 'transaction.html', {'form': form, 'purchase': purchase})


def checkout(request, pk):
    purchase = get_object_or_404(Purchase, pk=pk)

    if request.method == 'POST':
        form = CheckoutForm(request.POST, instance=purchase)
        if form.is_valid():
            purchase = form.save(commit=True)
            return redirect('checkout_complete')
    else:
        form = CheckoutForm(instance=purchase)
    return render(request, 'checkout.html', {'form': form, 'purchase': purchase})

def point_of_sale(request):
    return render(request, 'point_of_sale.html')

def checkout_complete(request):
    return render(request, 'checkout_complete.html')
