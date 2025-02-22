from store.models import Product, Category, Vendor, CartOrder, CartOrderItems, Wishlist, Tags, ProductImages, ProductReview, Address 
from userauths.models import Profile
from django.db.models import Min, Max
from django.contrib import messages

def default(request):
    categories = Category.objects.all()
    min_price = Product.objects.aggregate(Min('price'))
    max_price = Product.objects.aggregate(Max('price'))
    cart_total_amount = 0
    
    if 'cart_data_obj' in request.session:
        for product_id, product in request.session['cart_data_obj'].items():
            cart_total_amount += int(product['quantity']) * float(product['price'])
    else: 
        request.session['cart_data_obj'] = {}
            
    
    try:
        profile = Profile.objects.get(user=request.user)
    except:
        profile = None
    
    try:
        wishlist = Wishlist.objects.filter(user=request.user).count()
    except:
        wishlist = None
    
    try:
        address = Address.objects.get(user=request.user)
    except:
        address = None
        
    
    return {
        'categories': categories,
        'address': address,
        'wishlist': wishlist,
        'profile': profile,
        'min_price': min_price,
        'max_price': max_price,
        "cart_data": request.session['cart_data_obj'],
        'total_cart_items': len(request.session['cart_data_obj']),
    }