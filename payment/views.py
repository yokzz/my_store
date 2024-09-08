from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from store.models import CartOrder

@login_required
def payment_completed_view(request):
    cart_total_amount = 0
    
    order = CartOrder.objects.filter(user=request.user)
    
    if 'cart_data_obj' in request.session:
        for product_id, product in request.session['cart_data_obj'].items():
            cart_total_amount += int(product['quantity']) * float(product['price'])
    
    return render(request, "payment/payment-completed.html", {"cart_data": request.session['cart_data_obj'], 'total_cart_items': len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount, "order": order})

@login_required
def payment_failed_view(request):
    
    return render(request, 'payment/payment-failed.html')