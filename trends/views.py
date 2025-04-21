from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def placeholder_trends_view(request):
    return render(request, 'trends/trends.html')
