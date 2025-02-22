from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from store.models import CartOrder, CartOrderItems, Product, Category
from django.db.models import Sum
from django.contrib.auth.hashers import check_password

from userauths.models import User
from useradmin.forms import AddProductForm
from useradmin.decorators import admin_required

import datetime

@admin_required
def dashboard(request):
    total_orders_count = CartOrder.objects.filter(paid_status=True)
    all_products = Product.objects.all()
    all_categories = Category.objects.all()
    new_customers = User.objects.all().order_by("-id")
    latest_orders = CartOrder.objects.filter(paid_status=True).order_by("-order_date")
    
    this_month = datetime.datetime.now().month
    
    if CartOrder.objects.filter(paid_status=True).aggregate(price=Sum("price")) != None:
        revenue = CartOrder.objects.filter(paid_status=True).aggregate(price=Sum("price"))
    else:
        revenue = 0.00
    
    if CartOrder.objects.filter(order_date__month=this_month, paid_status=True).aggregate(price=Sum("price")) != None: 
        monthly_revenue = CartOrder.objects.filter(order_date__month=this_month, paid_status=True).aggregate(price=Sum("price"))
    else: 
        monthly_revenue = 0.00
    
    context = {
        "revenue": revenue,
        "total_orders_count": total_orders_count,
        "all_products": all_products,
        "all_categories": all_categories,
        "new_customers": new_customers,
        "latest_orders": latest_orders,
        "monthly_revenue": monthly_revenue,
    }
    
    return render(request, "useradmin/dashboard.html", context)

@admin_required
def products(request):
    all_products = Product.objects.all()
    all_categories = Category.objects.all()
    
    context = {
        "all_products": all_products,
        "all_categories": all_categories,
    }
    
    return render(request, "useradmin/products.html", context)

@admin_required
def add_product(request):
    if request.method == "POST":
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.save()
            messages.success(request, "Product added successfully!")
            return redirect("useradmin:products")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = AddProductForm()
            
    context = {
        "form": form,
    }
    return render(request, "useradmin/add-product.html", context)

@admin_required
def edit_product(request, pid):
    product = Product.objects.get(pid=pid)
    if request.method == "POST":
        form = AddProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.save()
            
            return redirect("useradmin:products")
    else:
        form = AddProductForm(instance=product)
            
    context = {
        "form": form,
        "product": product,
    }
            
    return render(request, "useradmin/edit-product.html", context)

@admin_required
def delete_product(request, pid):
    product = Product.objects.get(pid=pid)
    product.delete()
    
    return redirect("useradmin:products")

@admin_required
def orders(request):
    orders = CartOrder.objects.filter(paid_status=True)
    
    context = {
        "orders": orders
    }
    
    return render(request, "useradmin/orders.html", context)

@admin_required
def order_detail(request, id):
    order = CartOrder.objects.get(id=id)
    order_items = CartOrderItems.objects.filter(order=order)
    
    context = {
        "order": order,
        "order_items": order_items,
    }
    
    return render(request, "useradmin/order-detail.html", context)

@admin_required
def change_order_status(request, id):
    order = CartOrder.objects.get(id=id)
    if request.method == 'POST':
        status = request.POST["status"]
        print("status:", status)
        order.order_status = status
        order.save()
        messages.success(request, "Order status changed to {status}")
        
    return redirect("useradmin:order-detail", order.id)

@admin_required
def change_password(request):
    user = request.user
    
    if request.method == "POST":
        old_password = request.POST["old_password"]
        new_password = request.POST["new_password"]
        confirm_new_password = request.POST["confirm_new_password"]
        
        if new_password != confirm_new_password:
            messages.error(request, "Passwords do not match")
            return redirect("useradmin:change-password")
        
        elif old_password == new_password:
            messages.error(request, "Old and new passwords match")
            return redirect("useradmin:change-password")
            
        else:
            if check_password(old_password, user.password):
                user.set_password(new_password)
                user.save()
                messages.success(request, "Password has been changed successfully")
                return redirect("useradmin:change-password")
            
            else:
                messages.error(request, "Old password is incorrect")
                return redirect("useradmin:change-password")
            
    return render(request, "useradmin/change-password.html")