from django.urls import path, include
from customer.views import dashboard, order_detail, make_address_default


urlpatterns = [
    # Dashboard URL
    path("dashboard/", dashboard, name="dashboard"),

    # Order Detail URL
    path("dashboard/order/no-<int:id>", order_detail, name="order-detail"),

    # Making Address Default URL
    path("make-address-default", make_address_default, name="make-address-default")
]   

app_name = "customer"