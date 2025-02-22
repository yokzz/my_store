from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.db.models import Count, Avg
from django.template.loader import render_to_string
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.conf import settings
from django.core import serializers
import uuid
import json


from store.models import Product, Category, Vendor, CartOrder, CartOrderItems, Wishlist, Tags, ProductImages, ProductReview, Address, Coupon, ProductSpecifications
from userauths.models import Profile
from store.forms import ProductReviewForm



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
    profiles = Profile.objects.all()
    product_images = product.product_images.all()
    product_specifications = product.product_specifications.all()

    # Getting all reviews related to product
    reviews = ProductReview.objects.filter(product=product).order_by("-date")
    
    
    review_count = reviews.count()
    
    # Getting average rating
    average_rating = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))
    
    rating_distribution = reviews.values('rating').annotate(count=Count('id')).order_by('rating')
    
    # Prepare a dictionary to store percentage for each rating
    rating_percentages = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    
    for rating in rating_distribution:
        rating_percentages[rating['rating']] = (rating['count'] / review_count) * 100

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
        "profiles": profiles,
        "product_images": product_images,
        "product_specifications": product_specifications,
        "reviews": reviews,
        "review_form": review_form,
        'review_count': review_count,
        'rating_percentages': rating_percentages,
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
    profile_image = Profile.objects.get(user=user).image.url

    # if ProductReview.objects.filter(user=user, product=product).count() < 1:
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
    
    reviews = ProductReview.objects.filter(product=product).order_by("-date")
    
    review_count = reviews.count()
    
    rating_distribution = reviews.values('rating').annotate(count=Count('id')).order_by('rating')
    
    rating_percentages = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    
    for rating in rating_distribution:
        rating_percentages[rating['rating']] = (rating['count'] / review_count) * 100

    average_reviews = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))

    return JsonResponse(
        {
            'bool': True,
            'context': context,
            'avg_reviews': average_reviews,
            'profile_image': profile_image,
            "rating_prc": rating_percentages,
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
    product_id = str(request.GET['id'])
    
    cart_products[str(request.GET['id'])] = {
        'title': request.GET['title'], 
        'quantity': request.GET['quantity'],
        'price': request.GET['price'],
        'image': request.GET['image'],
        'pid': request.GET['pid'],
    }
    
    if 'cart_data_obj' in request.session:
        cart_data = request.session['cart_data_obj']
        if str(request.GET['id']) in cart_data:
            cart_data[str(request.GET['id'])]['quantity'] = int(cart_data[str(request.GET['id'])]['quantity']) + int(cart_products[str(request.GET['id'])]['quantity'])
        else:
            cart_data.update(cart_products)
        request.session['cart_data_obj'] = cart_data
            
    else:
        request.session['cart_data_obj'] = cart_products
        
    data = {
        "product_id": product_id,
        "product_title": cart_products[product_id]['title'],
        "product_price": cart_products[product_id]['price'],
        "product_image": cart_products[product_id]['image'],
        "quantity": cart_products[product_id]['quantity'],
        "total_cart_items": len(request.session['cart_data_obj']),
        "cart_data": request.session['cart_data_obj'],
    }
        
    return JsonResponse(data)

def cart_view(request):
    cart_total_amount = 0
    
    if request.user.is_authenticated:
        if CartOrder.objects.filter(user=request.user, paid_status=False).count() > 0:
            unpaid_orders = CartOrderItems.objects.filter(order__user=request.user, order__paid_status=False)
            unpaid_order = CartOrder.objects.filter(user=request.user, paid_status=False).last()
            unpaid_total = CartOrderItems.objects.filter(order__user=request.user, order__paid_status=False).first().order.price
        else:
            unpaid_total = None
            unpaid_order = None
            unpaid_orders = None
    else:
        unpaid_order = None
        unpaid_orders = None
        unpaid_total = None
        
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
                                                   'active_address': active_address,
                                                   'unpaid_order': unpaid_order,
                                                   'unpaid_orders': unpaid_orders,
                                                   'unpaid_total': unpaid_total})
    
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

def delete_from_side_cart(request):
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
    
    if request.user.is_authenticated:
        if CartOrder.objects.filter(user=request.user, paid_status=False).count() > 0:
            unpaid_orders = CartOrderItems.objects.filter(order__user=request.user, order__paid_status=False)
            unpaid_total = CartOrderItems.objects.filter(order__user=request.user, order__paid_status=False).first().order.price
        else:
            unpaid_total = None
            unpaid_orders = None
    else:
        unpaid_orders = None
        unpaid_total = None
    
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['quantity'] = quantity
            request.session['cart_data_obj'] = cart_data
            
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for product_id, product in request.session['cart_data_obj'].items():
            cart_total_amount += int(product['quantity']) * float(product['price'])
            
            try:
                active_address = Address.objects.get(user=request.user, status=True)
            except:
                active_address = None  
                
    
    context = {
        "cart_data": request.session['cart_data_obj'],
        'total_cart_items': len(request.session['cart_data_obj']),
        'cart_total_amount':cart_total_amount,
        'active_address': active_address,
        'unpaid_orders': unpaid_orders,
        'unpaid_total': unpaid_total,
    }
    
    data = render_to_string("store/async/cart-page.html", context, request)
    return JsonResponse({"data": data, 'total_cart_items': len(request.session['cart_data_obj'])})

def update_side_cart(request):
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
                
    
    context = {
        "cart_data": request.session['cart_data_obj'],
        'total_cart_items': len(request.session['cart_data_obj']),
        'cart_total_amount':cart_total_amount,
    }
    
    data = render_to_string("store/async/cart-page.html", context, request)
    return JsonResponse({"data": data, 'total_cart_items': len(request.session['cart_data_obj'])})

def save_checkout_info(request): 
    cart_total_amount = 0
    total_amount = 0

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
        
        if 'cart_data_obj' in request.session:
            cart_data = request.session['cart_data_obj']
            for product_id, product in cart_data.items():
                subtotal = int(product['quantity']) * float(product['price'])
                product['subtotal'] = subtotal
                total_amount += subtotal

            request.session['cart_data_obj'] = cart_data
            if request.user.is_authenticated:
                if CartOrder.objects.filter(user=request.user, paid_status=False).count() < 1:
                        order = CartOrder.objects.create(
                            user=request.user,
                            price=total_amount,
                            first_name=first_name,
                            last_name=last_name,
                            email=email,
                            phone_number=phone,
                            address=address,
                            city=city,
                            state=state,
                            country=country,
                            post_code=post_code,
                        )

                        for product_id, product in cart_data.items():
                            CartOrderItems.objects.create(
                                order=order,
                                invoice_number="INVOICE_NO-" + str(order.id),
                                product_id=product_id,
                                pid=product['pid'],
                                item=product['title'],
                                image=product['image'],
                                quantity=product['quantity'],
                                price=product['price'],
                                total=product['subtotal']
                            )

                        del request.session['first_name']
                        del request.session['last_name']
                        del request.session['email']
                        del request.session['phone']
                        del request.session['address']
                        del request.session['city']
                        del request.session['state']
                        del request.session['country']
                        del request.session['post_code']

                        return redirect("store:checkout", order.id)
                else:
                    messages.error(request, "You should first choose")
                    return redirect("store:cart")
            else:
                order = CartOrder.objects.create(
                            user=request.user,
                            price=total_amount,
                            first_name=first_name,
                            last_name=last_name,
                            email=email,
                            phone_number=phone,
                            address=address,
                            city=city,
                            state=state,
                            country=country,
                            post_code=post_code,
                        )

                for product_id, product in cart_data.items():
                    CartOrderItems.objects.create(
                        order=order,
                        invoice_number="INVOICE_NO-" + str(order.id),
                        product_id=product_id,
                        pid=product['pid'],
                        item=product['title'],
                        image=product['image'],
                        quantity=product['quantity'],
                        price=product['price'],
                        total=product['subtotal']
                    )

                del request.session['first_name']
                del request.session['last_name']
                del request.session['email']
                del request.session['phone']
                del request.session['address']
                del request.session['city']
                del request.session['state']
                del request.session['country']
                del request.session['post_code']

                return redirect("store:checkout", order.id)

def checkout_view(request, id):
    order = CartOrder.objects.get(id=id)
    orders = CartOrder.objects.filter(user=request.user)
    order_items = CartOrderItems.objects.filter(order=order)
    
    discount_amount = 0
    if request.method == "POST":
        data = json.loads(request.body)
        payment_method = data.get("fundingSource")
        
        print("method", payment_method)
        
        code = request.POST["code"]
        try:
            coupon = Coupon.objects.get(code=code, active=True)
        except Coupon.DoesNotExist: 
            coupon = None
            
        if coupon:
            for order_obj in orders:
                if coupon in order_obj.coupons.all():
                    messages.warning(request, "Coupon already activated")
                    return redirect("store:checkout", order.id)
                
            if coupon.uses <= coupon.use_count:
                messages.warning(request, "Coupon is expired")
                return redirect("store:checkout", order.id)
            
            else:
                discount_amount = order.price * coupon.discount / 100
                order.coupons.add(coupon)
                coupon.use_count += 1
                order.price -= discount_amount
                order.saved += discount_amount
                coupon.save()
                order.save()
                
                messages.success(request, "Coupon Activated")
                return redirect("store:checkout", order.id)
        else:
            messages.error(request, "Coupon does not exist")
    
    context = {
        "order": order,
        "order_items": order_items,
        "discount_amount": discount_amount,
    }
    
    return render(request, "store/checkout.html", context)
    
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

def delete_unpaid(request):
    delete_unpaid = CartOrder.objects.filter(user=request.user, paid_status=False).delete()
    
    return redirect("store:cart")

def edit_unpaid(request):
    unpaid_orders = CartOrderItems.objects.filter(order__user=request.user, order__paid_status=False)

    if 'cart_data_obj' in request.session:
        cart_data = request.session['cart_data_obj']

        for unpaid_order in unpaid_orders:
            title = unpaid_order.item
            quantity = unpaid_order.quantity
            price = float(unpaid_order.price)  
            image = unpaid_order.image
            product_id = str(unpaid_order.product_id)
            pid = unpaid_order.pid
            
            if product_id in cart_data:  
                cart_data[str(product_id)]['quantity'] = quantity
                cart_data.update(cart_data)
                request.session['cart_data_obj'] = cart_data
                
            else:
                cart_products = {}
                
                cart_products[str(product_id)] = {
                    'title': title, 
                    'quantity': quantity,
                    'price': price,
                    'image': image,
                    'pid': pid,
                }
                
                cart_data.update(cart_products)
        
        request.session['cart_data_obj'] = cart_data
                
                

        CartOrder.objects.get(user=request.user, paid_status=False).delete()
    
    return redirect("store:cart")