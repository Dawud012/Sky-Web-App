from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.urls import path
from . import views

urlpatterns = [

    path('', views.welcome_view, name='welcome'),
    

    path('login/', views.login_view, name='login'),
   
    path('logout/', views.logout_view, name='logout'),

     path('profile/', views.profile_view, name='profile'),
     
     path('register/', views.staff_register, name='staff-register'),

     path('trends/', include('trends.urls')),

     path('reset-password/', views.reset_password, name='reset-password'),
    
    path('reset-password/', auth_views.PasswordResetView.as_view(
        template_name='accounts/registration/password_reset_form.html',
        email_template_name='accounts/registration/password_reset_email.html',
        subject_template_name='accounts/registration/password_reset_subject.txt',
        success_url='/accounts/reset-password/done/'
    ), name='reset-password'),

    path('reset-password/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/registration/password_reset_done.html'
    ), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='accounts/registration/password_reset_confirm.html',
        success_url='/accounts/reset-password/complete/'
    ), name='password_reset_confirm'),

    path('reset-password/complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/registration/password_reset_complete.html'
    ), name='password_reset_complete'),

    
    
    
    path('trends/', include('trends.urls')),

]

