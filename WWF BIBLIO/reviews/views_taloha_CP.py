import mimetypes

from django.core.exceptions import MultipleObjectsReturned
from django.core.files.base import ContentFile
from django.http import HttpResponse, FileResponse
from django.shortcuts import render, redirect

from .forms import nouveaudocform
from .utils import average_rating
from .models import Book, Contributor
from account.views import get_logged_user_id
from django.core.paginator import Paginator

# Cette fonction book_list n'est pas egalement utile. Mais il est conseillé de ne pas l'effacer
def book_list(request):
    logged_user = get_logged_user_id(request)
    if logged_user :
        books = Book.objects.all()
        book_list = []
        for book in books:
            # Ces codes ne sont pas obligatoires
            reviews = book.review_set.all()
            if reviews:
                book_rating = average_rating([review.rating for review in reviews])
                number_of_reviews = len(reviews)
            else:
                book_rating = None
                number_of_reviews = 0

            book_list.append({'book': book, 'book_rating': book_rating, 'number_of_reviews': number_of_reviews})
        context = {'book_list': book_list}
        return render(request, 'books_list.html', context)
    else:
        return redirect('/login')

# Fonction recherche au niveau des formulaire de recherche
def recherche(request, valeur): # Nataoko ity methode ity satria tsy mot iray no hitdiavana fichier anaty base
    from django.db.models import Q

    # Créer une liste des mots clés
    keywords = valeur.split()  # Mot clé nosaratsarahina


    # Créer une liste d'expressions de requête pour chaque mot-clé
    queries_title = [Q(title__icontains=keyword) for keyword in keywords]
    queries_project_code = [Q(code_projet__icontains=keyword) for keyword in keywords]
    queries_theme = [Q(thématique__icontains=keyword) for keyword in keywords]
    queries_desc_mat = [Q(descripteur_matieres__icontains=keyword) for keyword in keywords]
    queries_annee = [Q(publication_date__icontains=keyword) for keyword in keywords]
        # toa izaon no fivoakan'ireo ==> [(title__icontains = teny), (title__icontains = tanana), ...] (mahazo liste)
        # arakaraka ny isan'ny teny voasoratra eo amin'ny champ de recherche ny isan'ny title__icontains azo

    # Combinez les expressions de requête en utilisant l'opérateur OR
    combined_query_title = queries_title.pop()
    combined_query_project_code = queries_project_code.pop()
    combined_query_theme = queries_theme.pop()
    combined_query_desc_mat = queries_desc_mat.pop()
    combined_query_publication_date = queries_annee.pop()

    for query in queries_title:
        combined_query_title |= query
    for query in queries_project_code:
        combined_query_project_code |= query
    for query in queries_theme:
        combined_query_theme |= query
    for query in queries_desc_mat:
        combined_query_desc_mat |= query
    for query in queries_annee:
        combined_query_publication_date |= query

    # Effectuer la recherche et retourner les résultats
    boky_by_title = Book.objects.filter(Q(combined_query_title))
    boky_by_project_code = Book.objects.filter(Q(combined_query_project_code))
    boky_by_theme= Book.objects.filter(Q(combined_query_theme))
    boky_by_desc_mat = Book.objects.filter(Q(combined_query_desc_mat))
    boky_by_pub_date = Book.objects.filter(Q(combined_query_publication_date))

    result_list_by_title = []
    result_list_by_project_code = []
    result_list_by_theme = []
    result_list_by_desc_mat = []
    result_list_by_pub_date = []
    total_result = []

    for book in boky_by_title:
        result_list_by_title.append(book)
        total_result.append(book)
    for book in boky_by_project_code:
        result_list_by_project_code.append(book)
        total_result.append(book)
    for book in boky_by_theme:
        result_list_by_theme.append(book)
        total_result.append(book)
    for book in boky_by_desc_mat:
        result_list_by_desc_mat.append(book)
        total_result.append(book)
    for book in boky_by_pub_date:
        result_list_by_pub_date.append(book)
        total_result.append(book)

    # Objet book daholo ireto en cas d'oubli
    return [
        result_list_by_title,
        result_list_by_project_code,
        result_list_by_theme,
        result_list_by_desc_mat,
        result_list_by_pub_date,
        total_result
    ]

# RAHA TSY NOSARATSARAHINA ILAY VALEUR NOMENA AVY EO AMIN'NY RECHERCHE
def recherche_brute(request, valeur):
    keywords_brute = valeur  # Mot clé tsy nosarahina
    result_brute_by_title = []
    result_brute_by_theme = []
    result_brute_by_desc_mat = []

    boky_by_title = Book.objects.filter(title__icontains = valeur)
    boky_by_theme = Book.objects.filter(thématique__icontains=valeur)
    boky_by_desc_mat = Book.objects.filter(descripteur_matieres__icontains=valeur)

    for book in boky_by_title:
        result_brute_by_title.append(book)
    for book in boky_by_theme:
        result_brute_by_theme.append(book)
    for book in boky_by_desc_mat:
        result_brute_by_desc_mat.append(book)

    return [result_brute_by_title,
            result_brute_by_theme,
            result_brute_by_desc_mat]


# Efa ilay ary anaty metadata (tableau) ity
def metadata(request):
    logged_user = get_logged_user_id(request)
    if logged_user:
        # Si un formulaire est rempli et est valide (Formulaire venant du champ recherche)
        if len(request.GET) > 0 :

            # Si il y a un element "2eRecherche" dans request.GET, les parametres GET vient du champ Recherche
            if "2eRecherche" in request.GET :
                # Chercher dans la base les documents ayant les informations fournis via le form de recherche
                # J'ai créé une  fonction appellé recherche (en cas d'oubli)
                resultat = recherche(request, request.GET["recherche"]) # Utilisation du fonction recherche

                # Pour la gestion de l'onglet actif
                if request.GET.get("pageAll"):
                    active_tab = "tab1"
                elif request.GET.get("pageCP"):
                    active_tab = "tab2"
                elif request.GET.get("pageTitle"):
                    active_tab = "tab3"
                elif request.GET.get("pageDescmat"):
                    active_tab = "tab4"

                else:
                    active_tab = None

                if active_tab is None:
                    active_tab = 'tab1'

                # ce contexte est inutile
                context = {
                    "book_list_by_title": resultat[0],
                    "book_list_by_project_code": resultat[1],
                    "book_list_by_theme": resultat[2],
                    "book_list_by_desc_geo": resultat[3],
                    "total_result": resultat[4]
                }
                print("context tab :", active_tab)

                print("context tab :", active_tab)

                # DJANGO DOC pagination =========================================
                # Pagination Code Projet ====================================================
                # Prendre les listes d'objet
                Objet_by_cp = resultat[1]

                # Chaque page est composé d'au plus 5 objets
                p = Paginator(Objet_by_cp, 10)

                # Prendre le numero de page envoyé via template
                page_number = request.GET.get("pageCP")

                # Prendre les objets correspondant au numero de page envoyé via template
                page_obj_by_cp = p.get_page(page_number)

                # Pagination titre =========================================================
                # Prendre les listes d'objet
                Objet_by_title = resultat[0]

                # Chage page est composé d'au plus 5 objets
                p_title = Paginator(Objet_by_title, 10)

                # Prendre le numero de page envoyé via template
                page_number_by_title = request.GET.get("pageTitle")

                # Prendre les objets correspondant au numero de page envoyé via template
                page_obj_by_title = p_title.get_page(page_number_by_title)

                # Pagination Theme ============================================
                # Prendre les listes d'objet
                Objet_by_theme = resultat[2]

                # Chage page est composé d'au plus 5 objets
                p_theme = Paginator(Objet_by_theme, 10)

                # Prendre le numero de page envoyé via template
                page_number_by_theme = request.GET.get("pageTheme")

                # Prendre les objets correspondant au numero de page envoyé via template
                page_obj_by_theme = p_theme.get_page(page_number_by_theme)

                # Pagination all ============================================
                # Prendre les listes d'objet
                all_obj = resultat[4]

                # Chage page est composé d'au plus 5 objets
                p_all = Paginator(all_obj, 10)  # page contenant tous les resultats obtenu des requetes

                # Prendre le numero de page envoyé via template
                page_number_by_all = request.GET.get("pageAll")

                # Prendre les objets correspondant au numero de page envoyé via template
                page_obj_by_all = p_all.get_page(page_number_by_all)

                # FIN PAGINATION =============================================================

                return render(request, "result_filtre.html", {"page_obj_by_CP": page_obj_by_cp,
                                                       "page_obj_by_title": page_obj_by_title,
                                                       "page_obj_by_theme": page_obj_by_theme,
                                                       "page_obj_by_all": page_obj_by_all,
                                                       "active_tab": active_tab,
                                                       "recherche": request.GET["recherche"]})

            # Sinon, les parametres GET est recu venant du template "result.html" (Il n'y a donc pas de "2eRecherche")

            else:
                if request.GET["title"] != "":
                    titre = request.GET["title"]
                    # En cas d'erreur, verifiez les espaces en trop
                    try :
                        boky = Book.objects.get(title=titre)

                    except MultipleObjectsReturned:
                        boky = Book.objects.filter(title=titre).first()

                    if boky :
                        # Prendre l'URL dans la base
                        objectChem = boky.url
                        chemin = r"{}".format(objectChem)
                        return render(request, "metadata.html", {"metadata": boky ,"chem": chemin})
                    else:
                        print(boky)

                else:
                    return render(request, "welcome.html")
        else:
            return render(request, "welcome.html")
    else :
        return redirect('/login')


# -----------------------------------------------------------------------------------------------------------
import os
import shutil

def importer_fichier(fichier_importe, objet):
    # Récupérer le chemin d'accès spécifié dans le champ "Chemin"
    chemin_cible = objet.Chemin

    # Vérifier si le dossier cible existe, sinon le créer
    if not os.path.exists(chemin_cible):
        os.makedirs(chemin_cible)

    # Déplacer le fichier vers le chemin cible
    nom_fichier = fichier_importe.name
    chemin_fichier = os.path.join(chemin_cible, nom_fichier)

    with open(fichier_importe.temporary_file_path(), 'rb') as f:
        contenu_fichier = f.read()
        with open(chemin_fichier, 'wb') as f_cible:
            f_cible.write(contenu_fichier)

    # Enregistrer le chemin du fichier dans le champ "fichier" du modèle
    objet.fichier.save(nom_fichier, ContentFile(contenu_fichier), save=True)


# insertion d'un nouveau document
def nouveaudoc(request):
    logged_user = get_logged_user_id(request)
    if logged_user:
        if len(request.GET) > 0:
            form = nouveaudocform(request.GET)
            if form.is_valid():

                form.save()
                return redirect("/welcome")
            else :
                print(request.POST)
                form = nouveaudocform(request.POST)
                return render(request, "nouveauDoc.html", {"form":form})
        else:
            form = nouveaudocform()
            return render(request, "nouveauDoc.html", {"form":form})
    else:
        return redirect("/login")




# Fonction de visualisation des fichiers
def view_file(request, chemin):
    from django.http import HttpResponse, Http404
    import os

    # Chemin d'accès complet au fichier PDF
    file_path = chemin

    # Vérifie si le fichier existe et est lisible

    file_name = os.path.basename(file_path)
    if file_name:
        content_type = mimetypes.guess_type(file_path)[0]
        try :
            with open(file_path, 'rb') as fh :
                response = HttpResponse(fh.read(), content_type=content_type)
                inline_types = ['text/plain',
                                'application/pdf',
                                'image/png',
                                'image/jpeg',
                                'image/gif',
                                'image/webp',
                                'audio/mpeg',
                                'audio/ogg',
                                'audio/wav',
                                'video/mp4',
                                'video/quicktime']
                # On telecharge direct si les fichiers ne peuvent pas etre lu sur le navigateur
                disposition = 'attachment' if content_type not in inline_types else 'inline'

                # Verification du taille si c'est un video
                if content_type.startswith('video/') and os.path.getsize(file_path) > 500 * 1024 * 1024:
                    return HttpResponse("La vidéo est trop grande pour être lue en streaming.", status=400)
                response['Content-Disposition'] = f'{disposition}; filename="{file_name}"'
                return response
        except FileNotFoundError:
            context = {'error_msg': f"Le fichier n'a pas été trouvé sur le disque."}
            return render(request, 'error.html', context=context)
    else:
        raise Http404