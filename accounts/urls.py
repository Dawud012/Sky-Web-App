from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
from django.urls import path, include


urlpatterns = [

    path('', views.welcome_view, name='welcome'),
    

    path('login/', views.login_view, name='login'),
   
    path('logout/', views.logout_view, name='logout'),

     path('profile/', views.profile_view, name='profile'),
     path('register/', views.register_view, name='register'),
     path('register/', views.staff_register, name='staff-register'),

     path('reset-password/', views.reset_password, name='reset-password'),
    path('trends/', include('trends.urls')),

]

