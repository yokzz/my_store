from django.db import models
from shopify_auth.models import AbstractShopUser
from userauths.models import User

class AuthAppShopUser(User, AbstractShopUser):
    pass