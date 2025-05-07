from django.contrib import admin
from customer.models import ContactUs

class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'subject']

admin.site.register(ContactUs, ContactUsAdmin)
