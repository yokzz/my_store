from django.urls import path, include
from useradmin.views import dashboard, products, add_product, edit_product, delete_product, orders, order_detail, change_order_status, change_password

urlpatterns = [
    # Dashboard URL
    path("dashboard/", dashboard, name='dashboard'),
    
    # Product List URL
    path("products/", products, name='products'),
    
    # Add, Edit, Delete Product URL
    path("product/add/", add_product, name='add-product'),
    path("product/edit/<pid>", edit_product, name='edit-product'),
    path("product/delete/<pid>", delete_product, name="delete-product"),
    
    # Orders URL
    path("orders/", orders, name="orders"),
    path("order/details/<id>/", order_detail, name="order-detail"),

    # Change Order Status URL
    path("order/status/change/<id>/", change_order_status, name="change-order-status"),

    # Change Password URL
    path("admin/password/change", change_password, name="change-password"),
]

app_name = "useradmin"
