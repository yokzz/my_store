from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import requests
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import logging

from store.models import CartOrder, CartOrderItems

from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received

logger = logging.getLogger(__name__)

@login_required
def payment_completed_view(request):
    cart_total_amount = 0
    total_amount = 0
    
    # Checking if cart_data_obj session still exists
    if 'cart_data_obj' in request.session: 
        # Getting total amount for paypal amount
        for product_id, product in request.session['cart_data_obj'].items():
            total_amount += int(product['quantity']) * float(product['price'])
        
        # order = CartOrder.objects.create(
        #         user=request.user,
        #         price = total_amount,
        #     )
    
        for product_id, product in request.session['cart_data_obj'].items():
            cart_total_amount += int(product['quantity']) * float(product['price']) 
            
            # cart_order_products = CartOrderItems.objects.create(
            #     order=order,
            #     invoice_number="INVOICE_NO-" + str(order.id),
            #     item=product['title'],
            #     image=product['image'],
            #     quantity=product['quantity'],
            #     price=product['price'],
            #     total=float(product['quantity']) * float(product['price'])
            # )
                
    order = CartOrder.objects.filter(user=request.user)
    
    return render(request, "payment/payment-completed.html", {"cart_data": request.session['cart_data_obj'], 'total_cart_items': len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount, "order": order})

@login_required
def payment_failed_view(request):
    
    return render(request, 'payment/payment-failed.html')

