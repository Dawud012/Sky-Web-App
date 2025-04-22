from django.urls import path
from . import views

urlpatterns = [
    path('', views.tutorial_view, name='tutorial'),
]
