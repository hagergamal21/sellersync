from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

# Home Page
def HomePage(request):
    return render(request, 'home.html')

# Login Page
def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home2')
        else:
             messages.error(request, 'Username or password is incorrect!')
             return render(request, 'login.html')
                
    return render(request, 'login.html')

# Register Page
def RegisterPage(request):
    if request.method=='POST' :
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')
        
        # Check if the provided data is valid
        if not uname or not email or not pass1 or not pass2:
            messages.error(request, 'Please fill in all fields!')
            return render(request, 'register.html')
        
        # Check if the username or email already exists
        if User.objects.filter(username=uname).exists():
            messages.error(request, 'Username already exists!')
            return render(request, 'register.html')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists!')
            return render(request, 'register.html')
        
        my_user = User.objects.create_user(username=uname, email=email, password=pass1)
        my_user.save()
        
        messages.success(request, 'Account created successfully! Please log in.')
        return redirect('home2')
        
    return render(request, 'register.html')

# Logout Page
def LogoutPage(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')


@login_required(login_url='/login/')
def home(request):
    return render(request, 'home2.html')


#reset Password
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.urls import reverse_lazy

class CustomPasswordResetView(PasswordResetView):
    template_name = "registration/password_reset_form.html"
    success_url = reverse_lazy("password_reset_done")

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = "registration/password_reset_done.html"

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "registration/password_reset_confirm.html"
    success_url = reverse_lazy("password_reset_complete")

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "registration/password_reset_complete.html"

