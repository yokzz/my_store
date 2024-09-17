from django.urls import path, include
from customer.views import dashboard, order_detail, make_address_default, contactus, ajax_contactus, profile_update


urlpatterns = [
    # Dashboard URL
    path("dashboard/", dashboard, name="dashboard"),

    # Order Detail URL
    path("dashboard/order/no-<int:id>", order_detail, name="order-detail"),

    # Making Address Default URL
    path("make-address-default", make_address_default, name="make-address-default"),

    # Contact Us URL
    path("contact-us", contactus, name="contact-us"),

    # Contact Us Ajax URL
    path("ajax-contact-us", ajax_contactus, name="ajax-contact-us"),

    # Profile Update
    path("profile/edit/", profile_update, name="profile-edit"),
]   

app_name = "customer"