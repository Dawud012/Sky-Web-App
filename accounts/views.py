from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import authenticate, login

def profile_view(request):
    return render(request, 'accounts/profile.html')
# Welcome page
def welcome_view(request):
    return render(request, 'accounts/welcome.html')

def reset_password(request):
    # your logic...
    return render(request, 'accounts/reset_password.html')

# Login page

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('start_voting')  # or whatever page you want
        else:
            messages.error(request, "Wrong email or password. Please try again.")

    return render(request, 'accounts/login.html')




# Logout (temp)
def logout_view(request):
    return render(request, 'accounts/login.html')  # update this later to actually log out

def staff_register(request):
    return render(request, 'accounts/register.html')

from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import render, redirect

def reset_password(request):
    email_sent = False

    if request.method == 'POST':
        email = request.POST.get('email')
        form = PasswordResetForm({'email': email})

        if form.is_valid():
            form.save(
                request=request,
                use_https=False,  # set to True if using HTTPS
                email_template_name='registration/password_reset_email.html',
                subject_template_name='registration/password_reset_subject.txt',
            )
            email_sent = True
            messages.success(request, "Password reset email sent!")
        else:
            messages.error(request, "That email address was not found.")

    return render(request, 'accounts/reset_password.html', {'email_sent': email_sent})










# Reset password page
# def reset_password(request):
   #  email_sent = False

    # if request.method == 'POST':
       #  email = request.POST.get('email')
        # simulate email sending
       #  email_sent = True
       #  messages.success(request, "Email sent")

    # return render(request, 'accounts/reset_password.html', {'email_sent': email_sent})

# ✅ Staff Registration view (handles form + saving to database)
def staff_register(request):
    if request.method == 'POST':
        full_name = request.POST.get('name')
        email = request.POST.get('email')
        password1 = request.POST.get('password')
        password2 = request.POST.get('confirm_password')

        # Check passwords match
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        # Check if email is already registered
        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('register')

        # Create user
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password1
        )
        user.first_name = full_name
        user.is_staff = True     # So it shows in Django admin's staff list
        user.is_active = True    # Just in case
        user.save()

        messages.success(request, "Account created successfully. You can now log in.")
        return redirect('login')

    return render(request, 'accounts/register.html')

def logout_view(request):
    return render(request, 'accounts/login.html')  # temporary

def register_view(request):
    return render(request, 'accounts/register.html')