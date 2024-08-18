from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db.models import Count, Avg

from store.models import Product, Category, Vendor, CartOrder, CartOrderItems, Wishlist, Tags, ProductImages, ProductReview, Address 
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
        "products": products
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

    context = {
        "product": product,
        "products": products,
        "product_images": product_images,
        "reviews": reviews,
        "review_form": review_form,
        'average_rating': average_rating,
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