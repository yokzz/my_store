from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.http import JsonResponse
from django.db.models.functions import ExtractMonth
from django.db.models import Count
from django.core import serializers
from django.template.loader import render_to_string

from store.models import CartOrder, CartOrderItems, Address
from customer.models import ContactUs
from userauths.models import Profile, User
from userauths.forms import ProfileForm

from allauth.socialaccount.models import SocialAccount


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
        country = request.POST["country"]
        state = request.POST["state"]
        
        new_address = Address.objects.create(
            user=request.user,
            address = address,
            phone_number = phone_number,
            city = city,
            post_code = post_code,
            country = country,
            state = state,
        )
        
        messages.success(request, "Address Added Successfully")
        
        
        
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
    order = CartOrder.objects.get(id=id)
    order_items = CartOrderItems.objects.filter(order=order)
    status_order = ["processing", "ontheway", "shipped", "delivered"]
    current_status = order.order_status

    active_statuses = status_order[:status_order.index(current_status) + 1]
    
    context = {
        "order": order,
        "order_items": order_items,
        'active_statuses': active_statuses,
    }
    
    return render(request, "customer/order-detail.html", context)

def make_address_default(request):
    id = request.GET['id']
    Address.objects.update(status=False)
    Address.objects.filter(id=id).update(status=True)
    return JsonResponse({"boolean": True})

def remove_address(request):
    id = request.GET['id']
    Address.objects.filter(id=id).delete()
    
    addresses = Address.objects.filter(user=request.user)
    
    context = {
        "bool": True,
        "address_obj": addresses
    }
    
    addresses_json = serializers.serialize('json', addresses)
    
    data = render_to_string("customer/async/address.html", context)
    
    return JsonResponse({"data": data, "addresses": addresses_json})

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
    user = request.user
    profile = Profile.objects.get(user=request.user)
    form = ProfileForm()
    
    orders = CartOrder.objects.annotate(month=ExtractMonth("order_date")).values("month").annotate(count=Count("id")).values("month", "count")
    month = []
    total_orders = []
    
    for order in orders:
        month.append(calendar.month_name[order['month']])
        total_orders.append(order['count'])
    
    if request.method == "POST":
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            try: 
                user.email = profile_form.cleaned_data.get('email')
                user.save()
                profile_form.save()
                messages.success(request, "Profile Edited Successfully.")
                return redirect("customer:dashboard")
            except: 
                messages.error(request, "Email already exists.")
                return redirect("customer:profile-edit")
    else:
        form = ProfileForm(instance=profile)
    
    context = {
        "profile": profile,
        "form": form,
        "month": month,
        "total_orders": total_orders,
    }
    
    return render(request, "customer/profile-edit.html", context)

@login_required
def change_password(request):
    user = request.user
    
    if request.method == "POST":
        old_password = request.POST["old_password"]
        new_password = request.POST["new_password"]
        confirm_new_password = request.POST["confirm_new_password"]
        
        if new_password != confirm_new_password:
            messages.error(request, "Passwords do not match")
            return redirect("customer:change-password")
        
        elif old_password == new_password:
            messages.error(request, "Old and new passwords match")
            return redirect("customer:change-password")
            
        else:
            if check_password(old_password, user.password):
                user.set_password(new_password)
                user.save()
                messages.success(request, "Password has been changed successfully")
                return redirect("customer:change-password")
            
            else:
                messages.error(request, "Old password is incorrect")
                return redirect("customer:change-password")
        
    return render(request, "customer/change-password.html")