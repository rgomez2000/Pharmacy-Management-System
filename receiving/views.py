from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from med_inventory.models import Order
from .forms import OrderForm

# Create your views here.
# Custom decorator to check if the user is in allowed groups
def allowed_groups(*groups):
    def in_groups(user):
            return user.groups.filter(name__in=groups).exists()
    return user_passes_test(in_groups)

# @login_required
# @allowed_groups('Pharmacy Manager')
def receiving_main(request):
    orders = Order.objects.all()
    return render(request, 'receiving_main.html', {'orders': orders})

# @login_required
def receive_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            drug = order.drug # Grabs the drug that is associated with the order being received
            drug.stock_qty += order.quantity # Add new inventory from receipt into the drug object
            drug.save()
            order_string = str(order) # Save off order string before we delete
            order.delete() # Delete Order
            messages.success(request, f'{order_string} successfully received.')
        return redirect('receiving_main')
    else:
        form = OrderForm(instance=order)  # Populate with existing data

    return render(request, 'receive_order.html', {'form': form, 'order': order})