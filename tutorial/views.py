from django.shortcuts import render

def tutorial_view(request):
    return render(request, 'tutorial/tutorial.html')
