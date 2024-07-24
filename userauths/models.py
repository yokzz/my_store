from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True, null=False)
    username = models.CharField(max_length=63)
    bio = models.CharField(max_length=63)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.email