from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .utils import validate_password, hash_password


# Home Page
def HomePage(request):
    return render(request, 'home.html')


# Login Page
def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home2')
        else:
            messages.error(request, 'Username or password is incorrect!')
            return render(request, 'login.html')

    return render(request, 'login.html')


# Register Page
def RegisterPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

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

        # Check if passwords match
        if pass1 != pass2:
            messages.error(request, "Passwords do not match!")
            return render(request, 'register.html')

        # Check password validation
        validation_result = validate_password(pass1)
        if validation_result != "Password is valid!":
            messages.error(request, validation_result)  # Show the validation error message
            return render(request, 'register.html')

        # If password is valid, hash the password
        hashed_password = hash_password(pass1)

        # Create the user
        try:
            user = User.objects.create_user(username=uname, email=email, password=hashed_password)
            user.save()
            messages.success(request, "Account created successfully!")
            return redirect('login')  # Redirect to the login page (or another page as needed)
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            return render(request, 'register.html')

    else:
        return render(request, 'register.html')


# Logout Page
def LogoutPage(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')


# Home Page (after login)
def home(request):
    return render(request, 'home2.html')


# Password validation and hashing view (for testing purposes)
def password_validation_and_hashing_view(request):
    if request.method == 'POST':
        password = request.POST.get('password')  # Get password from form
        validation_result = validate_password(password)  # Validate password

        if validation_result == "Password is valid!":
            hashed_password = hash_password(password)  # Hash the password if valid
            return render(request, 'result.html', {'result': "Password is valid and hashed!"})

        return render(request, 'result.html', {'result': validation_result})

    return render(request, 'password_form.html')

