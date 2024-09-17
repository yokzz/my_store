from django import forms
from customer.models import ContactUs

class ContactUsForm(forms.ModelForm):
    first_name = forms.CharField(max_length=63)
    last_name = forms.CharField(max_length=63)
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=63)
    subject = forms.CharField(max_length=63)
    message = forms.Textarea()
    

    class Meta:
        model = ContactUs
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'subject', 'message']