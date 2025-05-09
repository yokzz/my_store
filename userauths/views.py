from django.shortcuts import render, redirect
from userauths.forms import UserRegisterForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.conf import settings
from userauths.models import User

# User = settings.AUTH_USER_MODEL

def register_view(request):  
    if request.method == "POST":
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            messages.success(request, f"Hey {username}, You're account was created successfully")
            user = authenticate(username=form.cleaned_data['email'],
                                password=form.cleaned_data['password1'])
            login(request, user)
            return redirect("store:index")
    
    else:
        form = UserRegisterForm()
    
    
    context = {
        'form': form
    }
    
    return render(request, "userauths/sign-up.html", context)

def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request, f"Hey you are already logged in.")
        return redirect("store:index")
    
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, "You are logged in.")
                return redirect("store:index")
            
            else: 
                messages.error(request, "User does not exist. Create an account.")
            
        except:
            messages.error(request, f"User with {email} does not exist.")
        
            
        
    return render(request, "userauths/sign-in.html")

def logout_view(request):
    logout(request)
    messages.success(request, "You logged out")
    return redirect("userauths:sign-in")