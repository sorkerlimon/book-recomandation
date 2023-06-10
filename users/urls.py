from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('login-app/', login_app,name='login_app'),
    path('register/', register,name='register'),
    path('loginpage/', loginpage ,name='loginpage'),
    path('logout/', logoutuser ,name='logout'),

    

    path('activate/<uidb64>/<token>',activate, name='activate'),
   
    
]
