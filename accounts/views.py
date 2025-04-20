from django.shortcuts import render

def welcome_view(request):
    return render(request, 'accounts/welcome.html')



def staff_register(request):
    return render(request, 'accounts/register.html')


def login_view(request):
    return render(request, 'accounts/login.html')

def register_view(request):
    return render(request, 'accounts/register.html')

def logout_view(request):
    return render(request, 'accounts/login.html')  # temporary
