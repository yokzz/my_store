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

def product_detail_view(request, pid):
    product = Product.objects.get(pid=pid)
    products = Product.objects.filter(category=product.category).exclude(pid=pid)[:4]
    product_images = product.product_images.all()
    
    context = {
        "product": product,
        "products": products,
        "product_images": product_images,
    }
    
    return render(request, "store/product-detail.html", context)
    
def category_list_view(request):
    categories = Category.objects.all()
    # categories = Category.objects.all().annotate(product_count=Count("product"))
    
    context = {
        "categories": categories
    }
    
    return render(request, 'store/category-list.html', context)

def category_product_list_view(request, cid):
    category = Category.objects.get(cid=cid)
    products = Product.objects.filter(product_status="published", category=category)
    
    context = {
        "category": category,
        "products": products,
    }
    
    return render(request, "store/category-product-list.html", context)

def vendor_list_view(request):
    vendors = Vendor.objects.all()

    context = {
        "vendors": vendors,
    }
    
    return render(request, "store/vendor-list.html", context)

def vendor_detail_view(request, vid):
    vendor = Vendor.objects.get(vid=vid)
    products = Product.objects.filter(vendor=vendor, product_status="published")

    context = {
        "vendor": vendor,
        "products": products,
    }
    
    return render(request, "store/vendor-detail.html", context)

