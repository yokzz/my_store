from django.urls import path

from shopify_app.views import InitTokenRequestView, EndTokenRequestView

app_name = 'my_shopify_app'


urlpatterns = [
    path(
        'login-online/',
        InitTokenRequestView.as_view(
            redirect_path_name='my_shopify_app:end-token-request',
        ),
    ),
    path(
        'confirm/',
        EndTokenRequestView.as_view(
            redirect_path_name='embed_admin:dashboard',
        ),
        name='end-token-request'
    ),
]