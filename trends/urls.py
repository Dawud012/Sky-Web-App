from django.urls import path
from .views import placeholder_trends_view

urlpatterns = [
    path('', placeholder_trends_view, name='trends'),  
]
