from store.models import Product
from django import forms
from decimal import Decimal

class AddProductForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Enter product title"}))
    description = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Product description"}))
    price = forms.FloatField(widget=forms.NumberInput(attrs={"placeholder": "Sale Price"}))
    old_price = forms.FloatField(widget=forms.NumberInput(attrs={"placeholder": "Price without discount"}))
    specifications = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Product specifications"}))
    stock_count = forms.IntegerField(widget=forms.NumberInput(attrs={"placeholder": "12"}))
    
    
    class Meta:
        model = Product
        fields = [
            'title',
            'image',
            'description',
            'price',
            'old_price',
            'specifications',
            'stock_count',
            'product_status',
            'in_stock',
            'category',
            'vendor',
        ]
        
    def clean_price(self):
        price = self.cleaned_data['price']

        return round(Decimal(price), 2)
    
    def clean_old_price(self):
        old_price = self.cleaned_data['old_price']
        return round(Decimal(old_price), 2)