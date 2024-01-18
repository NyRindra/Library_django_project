"""wwfbiblio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views # Pour la reinitialisation de mdp

from account.views import log
from reviews.views import metadata, nouveaudoc, view_file
from .views import welcome, showrepertoire, download_batch_file, cp_th_ann, tous_les_documents

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", log),
    path("login/", log),
    path('welcome/', welcome),
    path('metadata/', metadata),
    path('affichage_cp_theme_annee/', cp_th_ann),
    path('nouveau/', nouveaudoc),
    path('tous/', tous_les_documents),
    path('', include("reviews.urls")),
    path('', include("account.urls")),



    # ====================== Vue pour les reinitialisations de mot de passe ============================================
    # Classe permettant de saisir l'adresse email du compte ayant oublié son mot de passe
    path('reset_password/', views.PasswordResetView.as_view( template_name = 'forget_password.html'), name = 'reset_password'),

    # classe qui se charge de l'envoie du mail
    path('reset_password_send/', views.PasswordResetDoneView.as_view(template_name = 'mailenvoyE.html' ), name='password_reset_done') ,

    # Classe pour la mis en place d'un nouveau mot de passe
    path('reset/<uidb64>/<token>', views.PasswordResetConfirmView.as_view(template_name = 'new_password.html'), name='password_reset_confirm'),

    #
    path('reset_password_complete', views.PasswordResetCompleteView.as_view(template_name = 'password_reset_success.html'), name='password_reset_complete'),

# ========================================= vue pour les visualisation des fichiers ==========================================================================

    
    # ny fonction dia afaka mandray parametre via path. io parametre io dia str...
    # Eto izany ny fonction view_file dia mahazo parametre "chemin".
    # Ary io parametre chemin io dia nampidiriko avy any amin'ny template ==> {% url 'view_pdf chemin=chem'%}
    path('view-pdfF/<path:chemin>', view_file, name='view_pdf'),
    path('batch/<path:chemin>/<str:titre>', download_batch_file, name='batch'),


    # Vue inutile (tsy miasa ito fa tsy fafaina )
    path('ma_vue/', showrepertoire, name='show'),  # Ce name sera utile dans Html
]
