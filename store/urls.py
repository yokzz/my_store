from django.urls import path
from store.views import index, category_list_view, product_list_view, product_detail_view, category_product_list_view, vendor_list_view, vendor_detail_view, ajax_add_review, search_view, product_filter_view, add_to_cart, cart_view, delete_from_cart, update_cart, checkout_view

urlpatterns = [
    # Home page URL
    path("", index, name="index"),
     
    # Product URL 
    path("products/", product_list_view, name="product-list"),
    path("products/<pid>/", product_detail_view, name="product-detail"),
    
    # Category URL
    path("category/", category_list_view, name="category-list"),
    path("category/<cid>/", category_product_list_view, name="category-product-list"),

    # Vendor URL
    path("vendor/", vendor_list_view, name="vendor-list"),
    path("vendor/<vid>", vendor_detail_view, name="vendor-detail"),

    # Add review URL
    path("ajax-add-review/<pid>/", ajax_add_review, name="ajax-add-review"),

    # Search URL
    path("search/", search_view, name="search"),
    
    # Filter Product URL
    path("filter-product/", product_filter_view, name="product-filter"),

    # Add to cart URL
    path("add-to-cart/", add_to_cart, name="add-to-cart"),

    # Delete from cart URL
    path("delete-from-cart/", delete_from_cart, name="delete-from-cart"),

    # Update cart URL
    path("update-cart", update_cart, name="update-cart"),

    # Cart URL
    path("view-cart/", cart_view, name="cart"),
    
    # Checkout URL
    path("checkout/", checkout_view, name="checkout"),
    
]

app_name = "store"