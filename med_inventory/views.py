from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from drugs.models import Drug
from django.core.cache import cache
from django.contrib import messages
from django.db.models import Sum
from med_inventory.models import Notification, Order
from django.utils import timezone
from datetime import timedelta
from logs.models import DrugDeletionLog, InventoryLog
from cashier.models import Receipt, PurchasedItemDetails, PurchasedPrescriptionDetails
from datetime import datetime

# Custom decorator to check if the user is in allowed groups
def allowed_groups(*groups):
    def in_groups(user):
            return user.groups.filter(name__in=groups).exists()
    return user_passes_test(in_groups)


# Threshold for low stock
LOW_STOCK_THRESHOLD = 120

@login_required
@allowed_groups('Pharmacist', 'Pharmacy Manager')
def inventory_check(request):
    cache.clear()
    drugs = Drug.objects.all()  # Fetch all drugs
    selected_drug = None
    stock_qty = None
    stock_status = None
    quantity_on_order = 0

    if request.method == 'GET' and 'drug' in request.GET and request.GET['drug']:
        selected_drug_id = request.GET['drug']
        selected_drug = get_object_or_404(Drug, id=selected_drug_id)
        stock_qty = selected_drug.stock_qty  
        stock_status = selected_drug.stock_status()  # Correctly call the method

# Determine stock status based on threshold
        stock_status = "In Stock" if stock_qty >= LOW_STOCK_THRESHOLD else "Low Stock"

# Calculate the total quantity currently on order for this drug
        quantity_on_order = Order.objects.filter(drug=selected_drug, fulfilled=False).aggregate(
            total_order=Sum('quantity')
        )['total_order'] or 0  # Defaults to 0 if no orders are found

    return render(request, 'inventory_check.html', {
        'drugs': drugs,
        'selected_drug': selected_drug,
        'stock_qty': stock_qty,
        'stock_status': stock_status,
        'quantity_on_order': quantity_on_order,
    })

@allowed_groups('Pharmacy Manager')
def manager_dash(request):
    # Clear old notifications to avoid duplicates
    Notification.objects.all().delete()

    # Retrieve all drugs
    drugs = Drug.objects.all()

    for drug in drugs:
        # Check each drug's stock level and create new notifications if stock is low
        if drug.stock_qty < LOW_STOCK_THRESHOLD:
            urgency = "High" if drug.stock_qty < LOW_STOCK_THRESHOLD / 2 else "Moderate"
            Notification.objects.create(
                drug=drug,
                stock_level=drug.stock_qty,
                urgency=urgency,
                notification_type = "stock"
            )
        
        # Check for expired drugs first.
        if drug.exp_date <= timezone.now().date():
            Notification.objects.create(
                drug = drug,
                urgency = "Expired",
                notification_type="expired",
            )
        # Check for the expiration date and create new notification if a drug expires within 30 days
        elif drug.exp_date <= timezone.now().date() + timedelta(days=30):
            if drug.exp_date <= timezone.now().date() + timedelta(days=7):
                urgency = "High"
            else:
                urgency = "Moderate"

            Notification.objects.create(
                drug = drug,
                urgency = urgency,
                notification_type = "expiring",
            )


    # Retrieve types of notifications for display
    low_stock_notifications = Notification.objects.filter(notification_type="stock").order_by('-created_at')
    expiring_notifications = Notification.objects.filter(notification_type="expiring").order_by('-created_at')
    expired_notifications = Notification.objects.filter(notification_type="expired").order_by('-created_at')

    # Render the template with all notification types
    return render(request, 'manager_dash.html', {
        'low_stock_notifications': low_stock_notifications,
        'expiring_notifications' : expiring_notifications,
        'expired_notifications': expired_notifications,
    })


# Delete the expired drug from the database
@allowed_groups('Pharmacy Manager')
def remove_expired_drug(request, drug_id):
    drug = get_object_or_404(Drug, id=drug_id)

    DrugDeletionLog.objects.create(
        deleted_by = request.user,
        drug_name = drug,
        event_type='deleted',
        description=f"Drug: {drug.drug_name} was deleted.",
    )

    drug.delete()  
    messages.success(request, f"The drug '{drug.drug_name}' has been removed from inventory.")
    return redirect('manager_dash')

@allowed_groups('Pharmacist', 'Pharmacy Manager')
def order_medication(request):
    if request.method == 'POST' and 'drug_id' in request.POST:
        drug_id = request.POST['drug_id']
        order_qty = int(request.POST['order_qty'])
        drug = get_object_or_404(Drug, id=drug_id)

        Order.objects.create(drug=drug, quantity=order_qty)
        
        # Set a success message
        messages.success(request, f"Order for {drug.drug_name} of {order_qty} units was successful!")
    return redirect ('inventory_check')

@allowed_groups('Pharmacy Manager')
def reports_main(request):

    cache.clear()
    report_type = None
    start_date = None
    end_date = None
    labels = []
    datasets = []
    if request.method == 'GET' and 'report_type' in request.GET:
        report_type = request.GET['report_type']
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']

        if report_type == "inventory":

            _logs = [_log for _log in InventoryLog.objects.all() if start_date <= datetime.strftime(_log.date, "%Y-%m-%d") <= end_date]
            _logs = sorted(_logs, key=lambda _log: _log.date)
            
            for log in reversed(_logs):
                if log.date not in labels:
                    labels.append(log.date)
                for data_set in datasets:
                    if data_set["label"] == log.item and len(data_set["data"]) != len(labels):
                        data_set["data"].insert(0, log.new_quantity)
                        break
                    elif data_set["label"] == log.item:
                        break
                else:
                    datasets.append({
                        "label": log.item,
                        "data": [log.new_quantity],
                        "borderWidth": 1
                    })
        
        elif report_type == "financial":
            # gather $ value sold by product each day
            _receipts = [_receipt for _receipt in Receipt.objects.all() if start_date <= datetime.strftime(_receipt.transaction_date.date(), "%Y-%m-%d") <= end_date]
            _receipts = sorted(_receipts, key=lambda _receipt: _receipt.transaction_date)

            for receipt in reversed(_receipts):
                if receipt.transaction_date.date() not in labels:
                    labels.append(receipt.transaction_date.date())
                
                for item in receipt.purchase.items.all():
                    details = PurchasedItemDetails.objects.get(item=item, purchase=receipt.purchase)
                    for data_set in datasets:
                        if data_set["label"] == item and len(data_set["data"]) != len(labels):
                            data_set["data"].insert(0, float(details.quantity*item.price))
                            break
                        elif data_set["label"] == item:
                            break
                    else:
                        datasets.append({
                            "label": item,
                            "data": [float(details.quantity*item.price)],
                            "borderWidth": 1
                        })
                
                for prescription in receipt.purchase.prescriptions.all():
                    details = PurchasedPrescriptionDetails.objects.get(prescription=prescription, purchase=receipt.purchase)
                    for data_set in datasets:
                        if data_set["label"] == prescription and len(data_set["data"]) != len(labels):
                            data_set["data"].insert(0, prescription.price)
                            break
                        elif data_set["label"] == prescription:
                            break
                    else:
                        datasets.append({
                            "label": prescription,
                            "data": [prescription.price],
                            "borderWidth": 1
                        })

    return render(request, 'reports.html', {
        'report_type': report_type,
        'start_date': start_date,
        'end_date': end_date,
        'labels': reversed(labels),
        'datasets': reversed(datasets)
    })