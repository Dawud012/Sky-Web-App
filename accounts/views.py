# Author : Dawud
# Co-Author : Parham Golmohammadi

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import authenticate, login, logout
from accounts.models import Profile
from voting.models import HealthCard 

# Welcome page
def welcome_view(request):
    return render(request, 'accounts/welcome.html')

# Public Registration view (defaults to Engineer)
def register_view(request):
    if request.method == 'POST':
        full_name = request.POST.get('name')
        email = request.POST.get('email')
        password1 = request.POST.get('password')
        password2 = request.POST.get('confirm_password')
        team = request.POST.get('team')
        department = request.POST.get('department')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('register')

        user = User.objects.create_user(username=email, email=email, password=password1)
        user.first_name = full_name
        user.save()
        # set default role
       

        # set default role using the constant
        profile = user.profile
        profile.role = Profile.ENGINEER
        profile.team = team
        profile.department = department
        profile.save()

        messages.success(request, "Account created successfully. You can now log in.")
        return redirect('login')

    return render(request, 'accounts/register.html')

# Staff Registration view (handles form + saving to database)
def staff_register(request):
    if request.method == 'POST':
        full_name = request.POST.get('name')
        email = request.POST.get('email')
        password1 = request.POST.get('password')
        password2 = request.POST.get('confirm_password')

        # Check passwords match
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('staff_register')

        # Check if email is already registered
        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('staff_register')

        # Create staff user
        user = User.objects.create_user(username=email, email=email, password=password1)
        user.first_name = full_name
        user.is_staff = True
        user.save()
        # grant admin role
        user.profile.role = Profile.ADMIN
        user.profile.save()

        messages.success(request, "Staff account created.")
        return redirect('login')

    return render(request, 'accounts/register.html')

# Login page
def login_view(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)

        if user:
            login(request, user)
            role = user.profile.role

            # engineers and team-leaders → voting
            if role in ('Engineer', 'Team Leader'):
                return redirect('start_voting')

           # dept-leaders & senior managers
            if role in ('Department Leader', 'Senior Manager'):
                return redirect('trends')

            # admin → django admin
            if user.is_staff:
                return redirect('admin:index')

        messages.error(request, "Invalid credentials")

    return render(request, 'accounts/login.html')



# Logout
def logout_view(request):
    logout(request)
    return redirect('login')

# Reset password page
def reset_password(request):
    email_sent = False

    if request.method == 'POST':
        email = request.POST.get('email')
        form = PasswordResetForm({'email': email})

        if form.is_valid():
            form.save(
                request=request,
                use_https=False,
                email_template_name='registration/password_reset_email.html',
                subject_template_name='registration/password_reset_subject.txt',
            )
            email_sent = True
            messages.success(request, "Password reset email sent!")
        else:
            messages.error(request, "That email address was not found.")

    return render(request, 'accounts/reset_password.html', {'email_sent': email_sent})

# Profile page
def profile_view(request):
    user = request.user
    prof = user.profile
    return render(request, 'accounts/profile.html', {
        'name': user.first_name,
        'email': user.email,
        'team': prof.team,
        'department': prof.department,
        'role': prof.role,
    })
