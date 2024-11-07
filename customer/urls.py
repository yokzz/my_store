from django.urls import path, include
from customer.views import dashboard, order_detail, make_address_default, contactus, ajax_contactus, profile_update, change_password, remove_address


urlpatterns = [
    # Dashboard URL
    path("dashboard/", dashboard, name="dashboard"),

    # Order Detail URL
    path("dashboard/order/no-<int:id>", order_detail, name="order-detail"),

    # Making Address Default URL
    path("make-address-default", make_address_default, name="make-address-default"),
    
    # Removing Address URL
    path("remove-address", remove_address, name="remove-address"),

    # Contact Us URL
    path("contact-us", contactus, name="contact-us"),

    # Contact Us Ajax URL
    path("ajax-contact-us", ajax_contactus, name="ajax-contact-us"),

    # Profile Update
    path("profile/edit/", profile_update, name="profile-edit"),
    
    # Change password URL
    path("profile/password/change/", change_password, name="change-password"),
]   

app_name = "customer"