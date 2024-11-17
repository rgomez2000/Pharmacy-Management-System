from django.shortcuts import redirect, render, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from .models import Purchase, PurchasedItemDetails
from .forms import PurchaseForm, CheckoutForm, PatientSelectForm, PrescriptionPurchaseForm
from django.contrib import messages

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
                # If yes, check if the newly requested quantity surpasses the amount we have in inventory
                if details.quantity + data["quantity"] > data["item"].quantity:
                    messages.error(request, f"Quantity requested surpasses amount available. Remaining inventory = {data['item'].quantity - details.quantity}")
                    return redirect(f'/purchasing/transaction/{purchase.id}')
                # If all good, update the quantity of that item in the purchase
                details.quantity += data["quantity"]
                details.save()
            except ObjectDoesNotExist:
                # if the item has not been added yet, create an instance of the through model PurchasedItemDetails
                # (but first, still need to check if requested quantity is allowed)
                if data["quantity"] > data["item"].quantity:
                    messages.error(request, f"Quantity requested surpasses amount available. Remaining inventory = {data['item'].quantity}")
                    return redirect(f'/purchasing/transaction/{purchase.id}')
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

def select_patient(request, pk=None):
    if pk is None: return
    purchase = get_object_or_404(Purchase, pk=pk)

    if request.method == 'POST':
        form = PatientSelectForm(request.POST, instance=purchase)
        if form.is_valid():
            purchase = form.save(commit=True)
            return redirect(f'/purchasing/prescription_transaction/{purchase.id}')
    else:
        form = PatientSelectForm(instance=purchase)
    return render(request, 'select_patient.html', {'form': form, 'purchase': purchase})

def prescription_transaction(request, pk=None):
    if pk is None: return
    purchase = get_object_or_404(Purchase, pk=pk)
    patient = purchase.patient

    if request.method == 'POST':
        form = PrescriptionPurchaseForm(request.POST, {"instance" : purchase, "patient" : patient})
        if form.is_valid():
            data = form.cleaned_data
            purchase.prescriptions.add(data["prescription"])
            # Calculate and update total cost for this purchase
            purchase.total_cost += data["prescription"].price
            # Update the quantity of the purchase with the total quantity of items added so far
            purchase.quantity_sold += 1
            # Save the changes
            purchase.save()
            # Return to normal transaction page
            return redirect(f'/purchasing/transaction/{purchase.id}')
    else:
        form = PrescriptionPurchaseForm()
    return render(request, 'prescription_transaction.html', {'form': form, 'purchase': purchase})

def checkout(request, pk):
    purchase = get_object_or_404(Purchase, pk=pk)

    if request.method == 'POST':
        form = CheckoutForm(request.POST, instance=purchase)
        if form.is_valid():
            purchase = form.save(commit=True)
            # Deduct all purchased items' quantities from their available stock
            for item in purchase.items.all():
                item.quantity -= item.purchaseditemdetails_set.get(purchase=purchase).quantity
                item.save()
            return redirect('checkout_complete')
    else:
        form = CheckoutForm(instance=purchase)
    return render(request, 'checkout.html', {'form': form, 'purchase': purchase})

def point_of_sale(request):
    return render(request, 'point_of_sale.html')

def checkout_complete(request):
    return render(request, 'checkout_complete.html')
