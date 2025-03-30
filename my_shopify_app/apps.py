from django.apps import AppConfig
from django.conf import settings
import shopify


class MyShopifyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'my_shopify_app'
    
    def ready(self):
        shopify.Session.setup(api_key=settings.SHOPIFY_API_KEY, secret=settings.SHOPIFY_API_SECRET)
