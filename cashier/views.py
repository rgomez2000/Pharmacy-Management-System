from django.shortcuts import redirect, render, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from .models import Purchase, PurchasedItemDetails, Receipt, PurchasedPrescriptionDetails
from .forms import PurchaseForm, PatientSelectForm, PrescriptionPurchaseForm, PaymentForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


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
        form = PrescriptionPurchaseForm(request.POST, instance=purchase)
        if form.is_valid():
            data = form.cleaned_data
            PurchasedPrescriptionDetails.objects.create(prescription=data["prescription"], purchase=purchase)
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
        form.filter_patient(patient)
    return render(request, 'prescription_transaction.html', {'form': form, 'purchase': purchase})

def checkout(request, pk):
    purchase = get_object_or_404(Purchase, pk=pk)
    change_due = None  # Initialize change_due to be None

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment_type = form.cleaned_data['payment_type']
            total_amount = purchase.total_cost

            # Check if a Receipt already exists for this Purchase
            receipt = Receipt.objects.filter(purchase=purchase).first()

            if receipt:
                # If a receipt already exists, show its details without creating a new one
                messages.warning(request, 'This transaction has already been finalized.')
                if receipt.payment_type == 'cash':
                    change_due = receipt.change  # Show the already calculated change
                return render(request, 'checkout.html', {'form': form, 'purchase': purchase, 'change_due': change_due})

            # Create a new Receipt if one doesn't exist
            receipt = Receipt(
                purchase=purchase,
                payment_type=payment_type,
                total_amount=total_amount,
                processed_by=request.user,  # Assign the logged-in user
            )

            if payment_type == 'cash':
                cash_given = form.cleaned_data['cash_given']
                if cash_given >= total_amount:
                    change_due = cash_given - total_amount
                    receipt.cash_given = cash_given
                    receipt.change = change_due
                    receipt.save()  # Save the receipt after populating required fields
                    messages.success(request, f'Transaction successful! Change due: ${change_due:.2f}')
                else:
                    messages.error(request, 'Insufficient cash provided. Please try again.')
                    return render(request, 'checkout.html', {'form': form, 'purchase': purchase, 'change_due': change_due})
            else:
                # Save receipt for card payment
                receipt.save()
                messages.success(request, f'{payment_type.capitalize()} payment processed successfully.')

            # Deduct stock quantities and update prescriptions
            for item in purchase.items.all():
                item.quantity -= item.purchaseditemdetails_set.get(purchase=purchase).quantity
                item.save()
            for prescription in purchase.prescriptions.all():
                prescription.picked_up = True
                prescription.save()

            # Redirect to the receipt detail page
            return redirect('receipt_detail', pk=purchase.id)
    else:
        form = PaymentForm()

    return render(request, 'checkout.html', {'form': form, 'purchase': purchase, 'change_due': change_due})

def point_of_sale(request):
    return render(request, 'point_of_sale.html')

def checkout_complete(request):
    return render(request, 'checkout_complete.html')

def receipt_detail(request, pk):
    receipt = get_object_or_404(Receipt, purchase__id=pk)
    return render(request, 'receipt_detail.html', {'receipt': receipt})