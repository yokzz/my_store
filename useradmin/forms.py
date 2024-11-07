from store.models import Product
from django import forms

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
        ]