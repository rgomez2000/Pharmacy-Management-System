from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from drugs.models import Drug
from django.core.cache import cache
from django.contrib import messages
from django.db.models import Sum
from med_inventory.models import Notification, Order

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

def manager_dash(request):
    # Clear old notifications to avoid duplicates
    Notification.objects.all().delete()

    # Check each drug's stock level and create new notifications if stock is low
    drugs = Drug.objects.all()
    for drug in drugs:
        if drug.stock_qty < LOW_STOCK_THRESHOLD:
            urgency = "High" if drug.stock_qty < LOW_STOCK_THRESHOLD / 2 else "Moderate"
            Notification.objects.create(
                drug=drug,
                stock_level=drug.stock_qty,
                urgency=urgency
            )

    # Retrieve notifications for display
    notifications = Notification.objects.all().order_by('-created_at')
    return render(request, 'manager.html', {
        'notifications': notifications,
    })


def order_medication(request):
    if request.method == 'POST' and 'drug_id' in request.POST:
        drug_id = request.POST['drug_id']
        order_qty = int(request.POST['order_qty'])
        drug = get_object_or_404(Drug, id=drug_id)

        Order.objects.create(drug=drug, quantity=order_qty)
        
        # Set a success message
        messages.success(request, f"Order for {drug.drug_name} of {order_qty} units was successful!")
    return redirect ('inventory_check')