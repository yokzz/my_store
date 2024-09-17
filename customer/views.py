from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models.functions import ExtractMonth
from django.db.models import Count

from store.models import CartOrder, CartOrderItems, Address
from customer.models import ContactUs
from userauths.models import Profile
from userauths.forms import ProfileForm

import calendar

@login_required
def dashboard(request):
    order_list = CartOrder.objects.filter(user=request.user).order_by("-order_date")
    address = Address.objects.filter(user=request.user)
    
    orders = CartOrder.objects.annotate(month=ExtractMonth("order_date")).values("month").annotate(count=Count("id")).values("month", "count")
    month = []
    total_orders = []
    
    for order in orders:
        month.append(calendar.month_name[order['month']])
        total_orders.append(order['count'])
    
    profile = Profile.objects.get(user=request.user)
    
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
        "order_list": order_list,
        "orders": orders,
        "address_obj": address,
        "profile": profile,
        "month": month,
        "total_orders": total_orders,
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

def contactus(request):
    
    return render(request, "customer/contactus.html")

def ajax_contactus(request):
    user = request.user
    
    contactus = ContactUs.objects.create(
        user=user,
        first_name=request.GET['first_name'],
        last_name=request.GET['last_name'],
        email=request.GET['email'],
        phone_number=request.GET['phone_number'],
        subject=request.GET['subject'],
        message=request.GET['message'],
    )
    
    context = {
        "bool": True,
    }
    
    return JsonResponse({"context": context})

def profile_update(request):
    profile = Profile.objects.get(user=request.user)
    form = ProfileForm()
    
    orders = CartOrder.objects.annotate(month=ExtractMonth("order_date")).values("month").annotate(count=Count("id")).values("month", "count")
    month = []
    total_orders = []
    
    for order in orders:
        month.append(calendar.month_name[order['month']])
        total_orders.append(order['count'])
    
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile_save = form.save(commit=False)
            profile_save.user = request.user
            profile_save.save()
            messages.success(request, "Profile Edited Successfully.")
            return redirect("customer:dashboard")
    else:
        form = ProfileForm(instance=profile)
    
    context = {
        "profile": profile,
        "form": form,
        "month": month,
        "total_orders": total_orders,
    }
    
    return render(request, "customer/profile-edit.html", context)