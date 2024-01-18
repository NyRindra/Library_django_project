from django.contrib import admin
from django.urls import path
from .views import log, nouveauCompte, voirmail



urlpatterns = [
    path('accounts/login/', log ),
    path('signin/', nouveauCompte),
    path('voirmail/', voirmail),

]