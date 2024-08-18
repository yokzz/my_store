from django.urls import path
from store.views import index, category_list_view, product_list_view, product_detail_view, category_product_list_view, vendor_list_view, vendor_detail_view, ajax_add_review

app_name = "store"

urlpatterns = [
    # Home page
    path("", index, name="index"),
    
    # Product 
    path("products/", product_list_view, name="product-list"),
    path("products/<pid>/", product_detail_view, name="product-detail"),
    
    # Category
    path("category/", category_list_view, name="category-list"),
    path("category/<cid>/", category_product_list_view, name="category-product-list"),

    # Vendor
    path("vendor/", vendor_list_view, name="vendor-list"),
    path("vendor/<vid>", vendor_detail_view, name="vendor-detail"),

    # Add review
    path("ajax-add-review/<pid>/", ajax_add_review, name="ajax-add-review"),
]
