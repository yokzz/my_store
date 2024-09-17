from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.db.models import Count, Avg
from django.template.loader import render_to_string
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.core import serializers
import uuid


from store.models import Product, Category, Vendor, CartOrder, CartOrderItems, Wishlist, Tags, ProductImages, ProductReview, Address, Coupon
from store.forms import ProductReviewForm

from paypal.standard.forms import PayPalPaymentsForm
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received



def index(request):
    products = Product.objects.filter(product_status="published", featured=True)
    
    context = {
        "products": products
    }
    
    return render(request, "store/index.html", context)

def product_list_view(request):
    products = Product.objects.filter(product_status="published")
    
    
    context = {
        "products": products,
    }
    
    return render(request, "store/product-list.html", context)   

def product_detail_view(request, pid):
    product = Product.objects.get(pid=pid)
    products = Product.objects.filter(category=product.category).exclude(pid=pid)[:4]
    product_images = product.product_images.all()

    # Getting all reviews related to product
    reviews = ProductReview.objects.filter(product=product).order_by("-date")
    
    # Getting average rating
    average_rating = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))

    # Product review form
    review_form = ProductReviewForm()
    
    make_review = True 
    
    if request.user.is_authenticated:
        user_review_count = ProductReview.objects.filter(user=request.user, product=product).count()

        if user_review_count > 0:
            make_review = False
            
    context = {
        "product": product,
        "products": products,
        "product_images": product_images,
        "reviews": reviews,
        "review_form": review_form,
        'average_rating': average_rating,
        "make_review": make_review,
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

def ajax_add_review(request, pid):
    product = Product.objects.get(pid=pid)
    user = request.user

    review = ProductReview.objects.create(
        user=user,
        product=product,
        review=request.POST['review'],
        rating=request.POST['rating'],
    )

    context = {
        "user": user.username,
        "review": request.POST['review'],
        "rating": request.POST['rating'],
    }

    average_reviews = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))

    return JsonResponse(
        {
            'bool': True,
            'context': context,
            'avg_reviews': average_reviews,
        }
    )
    
def search_view(request):
    query = request.GET["query"]
    
    products = Product.objects.filter(title__icontains=query).order_by("-date")
    
    context = {
        "products": products,
        "query": query,
    }
    
    return render(request, "store/search.html", context)

def product_filter_view(request):
    categories = request.GET.getlist('category[]')
    
    min_price = request.GET['min_price']
    max_price = request.GET['max_price']
    
    products = Product.objects.filter(product_status="published").order_by("id").distinct()
    
    products = products.filter(price__gte=min_price)
    products = products.filter(price__lte=max_price)
    
    if len(categories) > 0:
        products = products.filter(category__cid__in=categories).distinct() 
        
    data = render_to_string("store/async/product-list.html", {"products": products})
    
    return JsonResponse({"data": data}) 

def add_to_cart(request):
    cart_products = {}
    
    cart_products[str(request.GET['id'])] = {
        'title': request.GET['title'], 
        'quantity': request.GET['quantity'],
        'price': request.GET['price'],
        'image': request.GET['image'],
        'pid': request.GET['pid'],
    }
    
    if 'cart_data_obj' in request.session:
        if str(request.GET['id']) in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['quantity'] = int(cart_products[str(request.GET['id'])]['quantity'])
            cart_data.update(cart_data)
            request.session['cart_data_obj'] = cart_data
        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_products)
            request.session['cart_data_obj'] = cart_data
            
    else:
        request.session['cart_data_obj'] = cart_products
        
    return JsonResponse({"data": request.session['cart_data_obj'], 'total_cart_items': len(request.session['cart_data_obj'])})

def cart_view(request):
    cart_total_amount = 0
        
    if 'cart_data_obj' in request.session:
        for product_id, product in request.session['cart_data_obj'].items():
            cart_total_amount += int(product['quantity']) * float(product['price'])     
            
        try:
            active_address = Address.objects.get(user=request.user, status=True)
        except:
            active_address = None  
                
        
        return render(request, "store/cart.html", {"cart_data": request.session['cart_data_obj'],
                                                   'total_cart_items': len(request.session['cart_data_obj']), 
                                                   'cart_total_amount':cart_total_amount,
                                                   'active_address': active_address})
    
    else:
        return render(request, "store/cart.html", {'total_cart_items': 0, 'cart_total_amount': 0})
    
def delete_from_cart(request):
    product_id = str(request.GET['id'])
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            del request.session['cart_data_obj'][product_id]
            request.session['cart_data_obj'] = cart_data
            
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for product_id, product in request.session['cart_data_obj'].items():
            cart_total_amount += int(product['quantity']) * float(product['price'])
            
    
    data = render_to_string("store/async/cart-page.html", {"cart_data": request.session['cart_data_obj'], 'total_cart_items': len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount})
    return JsonResponse({"data": data, 'total_cart_items': len(request.session['cart_data_obj'])})

def update_cart(request):
    product_id = str(request.GET['id'])
    quantity = request.GET['quantity']
    
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['quantity'] = quantity
            request.session['cart_data_obj'] = cart_data
            
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for product_id, product in request.session['cart_data_obj'].items():
            cart_total_amount += int(product['quantity']) * float(product['price'])
            
    
    data = render_to_string("store/async/cart-page.html", {"cart_data": request.session['cart_data_obj'], 'total_cart_items': len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount})
    return JsonResponse({"data": data, 'total_cart_items': len(request.session['cart_data_obj'])})

def save_checkout_info(request):
   if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        address = request.POST["address"]
        city = request.POST["city"]
        state = request.POST["state"]
        country = request.POST["country"]
        post_code = request.POST["post_code"]
    
        request.session["first_name"] = first_name
        request.session["last_name"] = last_name
        request.session["email"] = email
        request.session["phone"] = phone
        request.session["address"] = address
        request.session["city"] = city
        request.session["state"] = state
        request.session["country"] = country
        request.session["post_code"] = post_code
        
        print(request.session["first_name"])
        
        return redirect("store:checkout")

def checkout_view(request):
    cart_total_amount = 0
    total_amount = 0
    
    if request.method == "POST":
        code = request.POST["code"]
        coupon = Coupon.objects.get(code=code, active=True)
    
    # Checking if cart_data_obj session still exists
    if 'cart_data_obj' in request.session: 
        # Getting total amount for paypal amount
        for product_id, product in request.session['cart_data_obj'].items():
            total_amount += int(product['quantity']) * float(product['price'])
            cart_total_amount += int(product['quantity']) * float(product['price'])    
        
        return render(request, "store/checkout.html", {
            "cart_data": request.session['cart_data_obj'],
            'total_cart_items': len(request.session['cart_data_obj']),
            'cart_total_amount': cart_total_amount,
        })
    
    else:
        return redirect("store:cart")
    
@login_required
def wishlist_view(request):
    try:
        wishlist_obj = Wishlist.objects.filter(user=request.user)
    except:
        messages.warning(request, "You have to login before using your wishlist")
        wishlist_obj = None
    
    context = {
        "wishlist_obj": wishlist_obj,
    }
    
    return render(request, "store/wishlist.html", context)
    
@login_required
def add_to_wishlist(request):
    id = request.GET['id']
    product = Product.objects.get(id=id)
    
    context = {
        "product": product
    }
    
    wishlist_count = Wishlist.objects.filter(product=product, user=request.user).count()
    print(wishlist_count)

    if wishlist_count > 0:
        context = {
            "bool": True
        }
    else:
        new_wishlist = Wishlist.objects.create(
            product=product,
            user=request.user
        )
    
        context = {
            "bool": True,
            "wishlist_count": Wishlist.objects.filter(user=request.user).count()
        }
    
    return JsonResponse(context)

@login_required
def remove_from_wishlist(request):
    id = request.GET['id']
    wishlist = Wishlist.objects.filter(user=request.user)
    
    product = Wishlist.objects.get(id=id)
    product_delete = product.delete()
    
    wishlist_count = wishlist.count()
    print(wishlist_count)
    
    context = {
        "bool": True,
        "wishlist_obj": wishlist,
        "wishlist_count": wishlist_count,
    }
    
    wishlist_json = serializers.serialize('json', wishlist)
    
    data = render_to_string("store/async/wishlist.html", context)
    
    return JsonResponse({"data": data, "wishlist": wishlist_json})

