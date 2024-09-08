from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse

from store.models import CartOrder, CartOrderItems, Address

@login_required
def dashboard(request):
    orders = CartOrder.objects.filter(user=request.user).order_by("-order_date")
    address = Address.objects.filter(user=request.user)
    
    if request.method == 'POST':
        address = request.POST["address"]
        phone_number = request.POST["phone"]
        city = request.POST["city"]
        post_code = request.POST["post_code"]
        
        new_address = Address.objects.create(
            user=request.user,
            address = address,
            phone_number = phone_number,
            city = city,
            post_code = post_code,
        )
        
        messages.success = (request, "Address Added Successfully")
        
        return redirect("customer:dashboard")
        
    context = {
        "orders": orders,
        "address_obj": address,
    }
    
    return render(request, 'customer/dashboard.html', context)

def order_detail(request, id):
    order = CartOrder.objects.get(user=request.user, id=id)
    products = CartOrderItems.objects.filter(order=order)
    
    context = {
        "order": order,
        "products": products,
    }
    
    return render(request, "customer/order-detail.html", context)

def make_address_default(request):
    id = request.GET['id']
    Address.objects.update(status=False)
    Address.objects.filter(id=id).update(status=True)
    return JsonResponse({"boolean": True})