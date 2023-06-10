from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', mainpage,name='mainpage'),
    path('search/', search_view, name='search'),
    path('book/<str:book_id>/', book_details_view, name='book_details'),
    path('dashboard/', dashboard, name='dashboard')

]
