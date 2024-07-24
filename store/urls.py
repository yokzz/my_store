from django.urls import path
from store.views import index, category_list_view, product_list_view

app_name = "store"

urlpatterns = [
    path("", index, name="index"),
    path("products/", product_list_view, name="product-list"),
    path("category/", category_list_view, name="category-list"),
]
