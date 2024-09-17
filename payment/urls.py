from django.urls import path, include
from payment.views import payment_completed_view, payment_failed_view, create_payment

urlpatterns = [
    # Paypal URL
    path('paypal/', include("paypal.standard.ipn.urls")),
    
    # Payment Create URL
    path('create_payment/', create_payment, name='create_payment'),
    
    # Payment Completed URL 
    path('payment-completed/', payment_completed_view, name="payment-completed"),
    
    # Payment Failed URL
    path('payment-failed/', payment_failed_view, name="payment-failed"),
]

app_name = "payment"