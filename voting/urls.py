from django.urls import path
from . import views

urlpatterns = [
    path('submit/', views.submit_vote, name='submit_vote'),
    path('summary/', views.vote_summary, name='vote_summary'),
]
