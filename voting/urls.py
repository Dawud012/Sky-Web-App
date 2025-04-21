from django.urls import path
from . import views

urlpatterns = [
    path('start/', views.start_voting, name='start_voting'),
    path('submit/<int:card_id>/', views.submit_vote, name='submit_vote'),
]