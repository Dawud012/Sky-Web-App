from django.urls import path
from . import views

urlpatterns = [
    path('', views.trends_page, name='trends'),
    path('<int:topic_id>/', views.topic_trends_view, name='topic_trend_detail'),
]
