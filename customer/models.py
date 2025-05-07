from django.db import models
from userauths.models import User

class ContactUs(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=63)
    email = models.EmailField()
    last_name = models.CharField(max_length=63)
    phone_number = models.CharField(max_length=63)
    subject = models.CharField(max_length=127)
    message = models.TextField()
    
    class Meta:
        verbose_name_plural = "Contact Us"
        
    def __str__(self):
        return self.last_name
