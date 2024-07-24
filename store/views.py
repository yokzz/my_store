from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Count

from store.models import Product, Category, Vendor, CartOrder, CartOrderItems, Wishlist, Tags, ProductImages, ProductReview, Address 


def index(request):
    products = Product.objects.filter(product_status="published", featured=True)
    
    context = {
        "products": products
    }
    
    return render(request, "store/index.html", context)

def product_list_view(request):
    products = Product.objects.filter(product_status="published")
    
    context = {
        "products": products
    }
    
    return render(request, "store/product-list.html", context)
    

def category_list_view(request):
    # categories = Category.objects.all()
    categories = Category.objects.all().annotate(product_count=Count("product"))
    
    context = {
        "categories": categories
    }
    
    return render(request, 'store/category-list.html', context)