from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import requests
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.urls import reverse

from store.models import CartOrder, CartOrderItems

from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received

import paypalrestsdk

paypalrestsdk.configure({
    "mode": "sandbox",
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_SECRET,
})

def create_payment(request):
    total_amount = 0
    
    if 'cart_data_obj' in request.session: 
        # Getting total amount for paypal amount
        for product_id, product in request.session['cart_data_obj'].items():
            total_amount += int(product['quantity']) * float(product['price'])
    
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal",
        },
        "redirect_urls": {
            "return_url": request.build_absolute_uri(reverse('payment:payment-completed')),
            "cancel_url": request.build_absolute_uri(reverse('payment:payment-failed')),
        },
        "transactions": [
            {
                "amount": {
                    "total": total_amount,  # Total amount in USD
                    "currency": "USD",
                },
                "description": "Payment for {product}",
            }
        ],
    })

    if payment.create():
        return redirect(payment.links[1].href)  # Redirect to PayPal for payment
    else:
        return render(request, 'payment/payment-failed.html')

def payment_completed_view(request):
    cart_total_amount = 0
    total_amount = 0
    
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')
    
    first_name = request.session.get("first_name")
    last_name = request.session.get("last_name")
    email = request.session.get("email")
    phone = request.session.get("phone")
    address = request.session.get("address")
    city = request.session.get("city")
    state = request.session.get("state")
    country = request.session.get("country")
    post_code = request.session.get("post_code")
    

    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        # Checking if cart_data_obj session still exists
        if 'cart_data_obj' in request.session: 
            # Getting total amount for paypal amount
            for product_id, product in request.session['cart_data_obj'].items():
                total_amount += int(product['quantity']) * float(product['price'])
            
            order = CartOrder.objects.create(
                    user=request.user,
                    price = total_amount,
                    paid_status = True,
                    first_name = first_name,
                    last_name = last_name,
                    email = email,
                    phone_number = phone,
                    address = address,
                    city = city,
                    state = state,
                    country = country,
                    post_code = post_code,
                )
        
            for product_id, product in request.session['cart_data_obj'].items():
                cart_total_amount += int(product['quantity']) * float(product['price']) 
                
                cart_order_products = CartOrderItems.objects.create(
                    order=order,
                    invoice_number="INVOICE_NO-" + str(order.id),
                    item=product['title'],
                    image=product['image'],
                    quantity=product['quantity'],
                    price=product['price'],
                    total=float(product['quantity']) * float(product['price'])
                )
                
                request.session['cart_data_obj'] = {}
                
        order = CartOrder.objects.filter(user=request.user)
        
        return render(request, 'payment/payment-completed.html', {"cart_data": cart_order_products, 'cart_total_amount':cart_total_amount, "order": order})
    else:
        return render(request, 'payment/payment_failed.html')
    

def payment_failed_view(request):
    
    return render(request, 'payment/payment-failed.html')

