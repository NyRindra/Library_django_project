from django.contrib import admin
from django.urls import path
from .views import book_list

urlpatterns = [
    path('booklist', book_list, name='welcome_view'),
]