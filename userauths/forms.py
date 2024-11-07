from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User, Profile


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Username"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Confirm password"}))
    
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "John"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Wash"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "josh.wash@gmail.com"}))
    bio = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Biography"}), required=False)
    phone_number = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "+1 (123) 456-7890"}))
    
    class Meta:
        model = Profile
        fields = ['image', 'first_name', 'last_name', 'email', 'bio', 'phone_number']