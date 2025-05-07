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


def payment_completed_view(request, id):
    request.session['cart_data_obj'] = {}
    order = CartOrder.objects.get(id=id)
    
    if not order.paid_status:
        order.paid_status = True
        order.save()
    
    context = {
        "order": order
    }
        
    return render(request, 'payment/payment-completed.html', context)

def payment_failed_view(request):
    return render(request, 'payment/payment-failed.html')

