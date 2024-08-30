from store.models import Product, Category, Vendor, CartOrder, CartOrderItems, Wishlist, Tags, ProductImages, ProductReview, Address 
from django.db.models import Min, Max

def default(request):
    categories = Category.objects.all()
    min_price = Product.objects.aggregate(Min('price'))
    max_price = Product.objects.aggregate(Max('price'))
    
    try:
        address = Address.objects.get(user=request.user)
    except:
        address = None
        
    
    return {
        'categories': categories,
        'address': address,
        'min_price': min_price,
        'max_price': max_price,
    }