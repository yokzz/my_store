from django.urls import path, include
from payment.views import payment_completed_view, payment_failed_view

urlpatterns = [
    # Paypal URL
    path('paypal/', include("paypal.standard.ipn.urls")),
    
    
    # Payment Completed URL 
    path('completed/<int:id>/', payment_completed_view, name="payment-completed"),
    
    # Payment Failed URL
    path('failed/', payment_failed_view, name="payment-failed"),
]

app_name = "payment"