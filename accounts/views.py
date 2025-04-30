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

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('register')

        user = User.objects.create_user(username=email, email=email, password=password1)
        user.first_name = full_name
        user.save()
        
        # set default role using the constant
        user.profile.role = Profile.ENGINEER
        user.profile.save()

        messages.success(request, "Account created successfully. You can now log in.")
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
            
            # Print debug info temporarily
            print(f"User logged in: {user.username}, Role: {user.profile.role}")
            
            # Check if superuser first (admin created via terminal)
            if user.is_superuser:
                return redirect('admin:index')
            
            # Get role from profile and use constants for comparison
            role = user.profile.role
            
            # Engineers and team-leaders → voting
            if role in (Profile.ENGINEER, Profile.TEAM_LEADER):
                return redirect('start_voting')

            # dept-leaders & senior managers → trends
            elif role in (Profile.DEPT_LEADER, Profile.SENIOR_MANAGER):
                return redirect('trends')

            # admin → django admin (only if they have staff permission)
            elif role == Profile.ADMIN and user.is_staff:
                return redirect('admin:index')
                
            # Default fallback - go to profile page
            else:
                return redirect('profile')

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