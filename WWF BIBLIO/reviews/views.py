import csv
import mimetypes

from django.core.exceptions import MultipleObjectsReturned
from django.core.files.base import ContentFile
from django.http import HttpResponse, FileResponse
from django.shortcuts import render, redirect

from .forms import nouveaudocform, form_csv
from .utils import average_rating
from .models import Book, Contributor, Langue, Type
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
    boky_by_theme = Book.objects.filter(Q(combined_query_theme))
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

        if book not in total_result:
            total_result.append(book)
        else:
            pass
    for book in boky_by_project_code:
        result_list_by_project_code.append(book)
        if book not in total_result:
            total_result.append(book)
        else:
            pass
    for book in boky_by_theme:
        result_list_by_theme.append(book)
        if book not in total_result:
            total_result.append(book)
        else:
            pass
    for book in boky_by_desc_mat:
        result_list_by_desc_mat.append(book)
        if book not in total_result:
            total_result.append(book)
        else:
            pass
    for book in boky_by_pub_date:
        result_list_by_pub_date.append(book)
        if book not in total_result:
            total_result.append(book)
        else:
            pass

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

    boky_by_title = Book.objects.filter(title__icontains = keywords_brute)
    boky_by_theme = Book.objects.filter(thématique__icontains=keywords_brute)
    boky_by_desc_mat = Book.objects.filter(descripteur_matieres__icontains=keywords_brute)

    print("resultat brute eee:", boky_by_title)

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
                if request.GET.get("pageAll"):
                    active_tab = "tab1"
                elif request.GET.get("pageCP"):
                    active_tab = "tab2"
                elif request.GET.get("pageTitle"):
                    active_tab = "tab3"
                elif request.GET.get("pageDescmat"):
                    active_tab = "tab4"
                elif request.GET.get("pageTheme"):
                    active_tab = "tab5"

                else:
                    active_tab = None

                if active_tab is None:
                    active_tab = 'tab1'
                # ============================================================================

                # RECHERCHE ET TRIAGE PAR ORDRE DE RECHERCHE =================================
                # Utilisation de la fonction recherche
                champ_recherche = request.GET["recherche"].strip()  # Suppression des espace en avant et en arriere
                resultat_recherche = recherche(request, champ_recherche)
                resultat = resultat_recherche

                # ORDRE DE PRIORITE D'AFFICHAGE
                # Utilisation de fonction recherche_brute()... ilay tsy zaraina ny entrée
                resultat_recherche_brute = recherche_brute(request, champ_recherche)
                resultat_brute = resultat_recherche_brute
                if len(resultat_brute[0]) != 0:  # Resultat brute liste
                    compteur = 0
                    for boky in resultat_brute[0]:
                        if boky in resultat[5]:
                            resultat[5].remove(boky)
                            resultat[5].insert(compteur, boky)
                            compteur += 1
                if len(resultat_brute[1]) != 0:  # Resultat brute liste
                    compteur = 0
                    for boky in resultat_brute[1]:
                        if boky in resultat[5]:
                            resultat[5].remove(boky)
                            resultat[5].insert(compteur, boky)
                            compteur += 1
                if len(resultat_brute[2]) != 0:  # Resultat brute liste
                    compteur = 0
                    for boky in resultat_brute[2]:
                        if boky in resultat[5]:
                            resultat[5].remove(boky)
                            resultat[5].insert(compteur, boky)
                            compteur += 1

                # ========================================================================

                # DJANGO DOC pagination ==================================================
                # Pagination all ============================================
                # Prendre les listes d'objet
                all_obj = resultat[5]

                # Chage page est composé d'au plus 5 objets
                p_all = Paginator(all_obj, 10)  # page contenant tous les resultats obtenu des requetes

                # Prendre le numero de page envoyé via template
                page_number_by_all = request.GET.get("pageAll")

                # Prendre les objets correspondant au numero de page envoyé via template
                page_obj_by_all = p_all.get_page(page_number_by_all)

                # PAGINATION TITRE (TSY MIASA FA AZA FAFAINA )=====================================================
                # Prendre les listes d'objet
                Objet_by_title = resultat[0]

                # Chage page est composé d'au plus 10 objets
                p_title = Paginator(Objet_by_title, 30)

                # Prendre le numero de page envoyé via template
                page_number_by_title = request.GET.get("pageTitle")

                # Prendre les objets correspondant au numero de page envoyé via template
                page_obj_by_title = p_title.get_page(page_number_by_title)

                # PAHINATION THEME (TSY MIASA FA AZA FAFAINA )============================================
                # Prendre les listes d'objet
                Objet_by_theme = resultat[2]

                # Chage page est composé d'au plus 10 objets
                p_theme = Paginator(Objet_by_theme, 10)

                # Prendre le numero de page envoyé via template
                page_number_by_theme = request.GET.get("pageTheme")

                # Prendre les objets correspondant au numero de page envoyé via template
                page_obj_by_theme = p_theme.get_page(page_number_by_theme)

                # TSY NAMPIASA PAGINATION INTSONY AHO NANOMBOKA TETO____________________________________________________
                # CODE Projet ============================================================
                # Prendre les listes d'objet
                cp_result = resultat[1]  # Ilay fonction recherche()

                # Alaina daholo ny cp an'ireo objet
                liste_cp = []
                for objet in cp_result:
                    if objet.code_projet not in liste_cp:
                        if "|" in objet.code_projet:
                            cp_misaraka = objet.code_projet.split("|")
                            for item in cp_misaraka:
                                if item in liste_cp:
                                    pass
                                else:
                                    liste_cp.append(item)
                        else:
                            liste_cp.append(objet.code_projet)
                    else:
                        pass

                # Diovina kely ilay cp sao misy espace avant na apres
                LISTE_cp = []
                for cp in liste_cp:
                    Espace_avant_apres = cp.strip()  # manala espace supplementaire avant et apres
                    # if " " in Espace_avant_apres:
                    # Espace_avant_apres = Espace_avant_apres.replace(" ", "")
                    LISTE_cp.append(Espace_avant_apres)
                print("liste cp", LISTE_cp)

                # Alaina ny cp 6 caracteres mba hi creer-na dossier
                CP_vaovao = []

                for CP in LISTE_cp:

                    if "." in CP:
                        index = CP.find(".")
                        s = ''.join(CP[x] for x in range(len(CP)) if x < index)
                        CP_vaovao.append(s)
                    else:
                        if len(CP) == 8:
                            s = ''.join(CP[x] for x in range(len(CP)) if x < 6)
                            CP_vaovao.append(s)
                        elif len(CP) < 8:
                            CP_vaovao.append(CP)
                        else:
                            CP_vaovao.append(CP)
                # Iny CP_vaovao iny no entina miditra ao amin'ny pagination django

                Objet_by_cp = sorted(CP_vaovao, key=lambda x: int(x[2:]))  # Triage alphabetique
                final_cp = Objet_by_cp  # CP final no ampiasaiko satria tsy ampiasa pagination aho
                # (sao mbola hiverina ampiasa dia tsy tiako kitihina ilay Objet_by_cp )
                print("Objet_by_cp", Objet_by_cp)
                NOMBRE_DE_LIVRE_PAP_cp = []
                for item in Objet_by_cp:
                    livre = Book.objects.filter(code_projet__icontains=item)
                    nombredulivre = len(livre)
                    NOMBRE_DE_LIVRE_PAP_cp.append(nombredulivre)

                # Chaque page est composé d'au plus 10 objets
                p_cp = Paginator(Objet_by_cp, 10)  # tsy nampiasaina ity pagination ity ho an'ny CP

                # Prendre le numero de page envoyé via template
                page_number = request.GET.get("pageCP")

                # Prendre les objets correspondant au numero de page envoyé via template
                page_obj_by_cp = p_cp.get_page(page_number)

                # =====================TAPITRA ETO NY THEME MISY PAGINATION==============

                # Theme tsy misy pagination ito manaraka ito =======================================
                # Alaina ny thematique rehetra

                theme_des_objets = []
                for i in resultat[2]:
                    theme_des_objets.append(i.thématique)
                list_theme = []
                for i in theme_des_objets:
                    # alaina ny theme rehetra raha misy boky manana theme maromaro (nampiasa | i ranja)
                    if "|" in i:
                        theme_separé = i.split("|")  # lasa mahazo liste ["theme1", "theme2", "theme3", ...]
                        for i in theme_separé:
                            i_sans_espace = i.strip()
                            if i_sans_espace in list_theme:
                                pass
                            else:
                                list_theme.append(i_sans_espace)
                    else:
                        i_sans_espace = i.strip()
                        if i_sans_espace in list_theme:
                            pass
                        else:
                            list_theme.append(i_sans_espace)
                print("list theme :", list_theme)
                NOMBRE_DE_LIVRE_PAP_th = []
                for item in list_theme:
                    livre = Book.objects.filter(thématique__icontains=item)
                    nbr_livre_th = len(livre)
                    NOMBRE_DE_LIVRE_PAP_th.append(nbr_livre_th)
                print("nbr par theme :", NOMBRE_DE_LIVRE_PAP_th)
                # if not list_theme: azo tester-na toa izao iny liste raha vide na tsia
                # ==================================================================================

                # FIN PAGINATION =============================================================

                # Sortie vers le template :
                if page_obj_by_title:  # Misy page obj ve? tsy misy io raha vide ilay resultat[0] avy @ recherche
                    print("obj_be title", page_obj_by_title)

                else:
                    print(Objet_by_title)
                    print("tsisy")
                # raha vide ilay objet avy any amin'ny fonction recherche ka manao if page_obj_by_title dia
                # lasa mankany amin'ny else izy (io ambony anaty if io ny test nataoko)

                CONTEXT = {"page_obj_by_CP": page_obj_by_cp,
                           "page_obj_by_title": page_obj_by_title,
                           "page_obj_by_theme": page_obj_by_theme,
                           "page_obj_by_all": page_obj_by_all,
                           "active_tab": active_tab,
                           "recherche": request.GET["recherche"], }

                if logged_user.is_admin == True:
                    CONTEXT["logged_user_is_admin"] = "True"
                if len(final_cp) != 0 and len(NOMBRE_DE_LIVRE_PAP_cp) != 0:
                    # Atao anaty ny liste roa raha te hampiasa azy miaraka anaty boucle de template
                    CONTEXT["ZIP_CP"] = zip(final_cp, NOMBRE_DE_LIVRE_PAP_cp)
                if len(list_theme) != 0 and len(NOMBRE_DE_LIVRE_PAP_th) != 0:
                    CONTEXT["ZIP_TH"] = zip(list_theme, NOMBRE_DE_LIVRE_PAP_th)
                return render(request, "result_filtre.html", CONTEXT)

            # Sinon, les parametres GET est recu venant du template "result.html" (Il n'y a donc pas de "2eRecherche")

            else:
                if request.GET["title"] != "":
                    titre = request.GET["title"]
                    id = request.GET["id"]
                    # En cas d'erreur, verifiez les espaces en trop
                    try :
                        boky = Book.objects.get(title=titre, id=id)

                    except MultipleObjectsReturned:
                        boky = Book.objects.filter(title=titre).first()

                    if boky :
                        # Prendre l'URL dans la base
                        objectChem = boky.lien
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

# Tsy miasa ito fonction ito
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


# insertion d'un nouveau document (FORMULAIRE OU CSV)
def nouveaudoc(request):
    logged_user = get_logged_user_id(request)
    if logged_user:
        # Raha tsy admin tsy afaka mi-ajouter document
        if logged_user.is_admin == True or logged_user.admin_doc == True or logged_user.niveau_1 == True :
            if len(request.POST) > 0 :
                if request.method == 'POST':
                    if request.POST['form_type'] == 'Formulaire' :
                        form = nouveaudocform(request.POST, request.FILES)
                        form_CSV = form_csv()
                        print("LIEN OOOOOOOOOO")

                        if form.is_valid():
                            # Ajouter le nom de fichier au lien
                            nom_fichier = request.FILES['fichier'].name
                            lien = form.cleaned_data['lien']
                            lien_complet = os.path.join(lien, nom_fichier)

                            form.instance.lien = lien_complet   # Modifier-na ny lien (lasa lien nomena
                                                                # teo am formulaire + nom du fichier)
                            form.instance.utilisateur_resp_id = logged_user.id
                            # Enregistrer le formulaire et copier le fichier sur l'ordinateur distant

                            # Écrire le fichier sur le disque
                            fichier = form.cleaned_data['fichier']
                            with open(lien_complet, 'wb+') as destination:
                                for chunk in fichier.chunks():
                                    destination.write(chunk)
                            form.save()

                            # Rediriger vers la page de confirmation
                            return render(request, 'confirmation.html')

                        else:
                            print("tsy validess")

                            # Ca m'a pris 1 jour : L"OUBLIE DE CE REQUEST.FILES EST IMPORTANT
                            # POUR AFFICHER L'ERREUR AU NIVEAU DU CHAMP FI
                            form = nouveaudocform(request.POST, request.FILES)
                            return render(request, 'nouveauDoc.html', {'form': form, "form_csv": form_CSV})

                    elif request.POST['form_type'] == 'CSV' :
                        form_CSV = form_csv(request.POST, request.FILES)
                        if form_CSV.is_valid() :
                            csv_file = form_CSV.cleaned_data['csv_file']
                            csv_data = csv_file.read().decode('utf-8')

                            sauvegared = save_csv_data(request, csv_data)
                            if type(sauvegared) is list:
                                return render(request, 'error.html', {'error_msg': sauvegared[1]})
                            elif sauvegared == "10 element au maximum" :
                                return render(request, 'error.html', {'error_msg': 'Vous pouvez remplir au plus 10 lignes dans le CSV'})
                            else:
                                return redirect('/poinsa')
                        else :
                            form_CSV = form_csv(request.POST, request.FILES)
                            form = nouveaudocform()
                            return render(request, 'nouveauDoc.html', {'form': form, "form_csv": form_CSV})
                else:
                    form = nouveaudocform()
                    form_CSV = form_csv()
                    return render(request, 'nouveauDoc.html', {'form': form, "form_csv": form_CSV})
            else:
                form = nouveaudocform()
                form_CSV = form_csv()
                return render(request, 'nouveauDoc.html', {'form': form, "form_csv": form_CSV})
        else:
            return redirect("/welcome")
    else:
        return redirect("/login")

def save_csv_data(request, csv_data):
    logged_user = get_logged_user_id(request)
    # Utilisez csv.reader pour lire les données du CSV
    csv_reader = csv.reader(csv_data.splitlines(), delimiter=';')

    # Ignorez la première ligne du CSV (entête)
    next(csv_reader)

    # Parcourez chaque ligne du CSV et créez un nouveau livre dans la base de données

        # Fomba fakana dernier element dans la base de données
    boky_farany = Book.objects.latest('id') #ilaiko satria ampidiriko anaty base ny ID
    id_farany = boky_farany.id
    id_tohiny = id_farany + 1 # Ny id tokony ho soratana izany raha io ambony ny farany ao
    print("id farany", id_farany)
        # Compteur de boucle
    compteur = 2

    # Coupure du boucle au bout de 10 elements ajouté
    for row in csv_reader:
        if compteur > 11 :
            return "10 element au maximum"
            break
        # raha sendra misy erreur tafiditra toa io anatin'ilay chemin
        row = [item.lstrip('\u202a') for item in row]
        try:
            # Récupérez les valeurs de chaque colonne du CSV
            code_projet = row[0].strip()
            titre = row[1].strip()
            if not titre or type(titre) is not str:
                raise ValueError('Veuillez mettre un titre valide')
            langue_str = row[2].strip()
            if langue_str == "FR":
                langue_id = 1
            elif langue_str == "EN":
                langue_id = 2
            elif langue_str == "MG":
                langue_id = 3
            elif "/" in langue_str :
                first_element = langue_str.split('/')[0].strip()
                if first_element == "FR":
                    langue_id = 1
                elif first_element == "EN":
                    langue_id = 2
                elif first_element == "MG":
                    langue_id = 3
                # Gérer le cas où la langue n'est pas valide
            else :
                raise ValueError("La langue n'est pas valide")

            # Années de publication =========================
            date_pub = row[3].strip()
            if date_pub :
                try :
                    date = int(date_pub)
                except:
                    print("type int", type(date_pub))
                    raise ValueError("Verifier l'année que vous avez entré")
                else:
                    if int(date_pub) > 2100 or int(date_pub) < 1900 :
                        raise ValueError("Entrez une date valide")
                    else:
                        pass

            else :

                date_pub = None

            descripteur = row[4].strip()
            auteur = row[5].strip()
            niveau_biblio = row[6].strip()
            thematique = row[7]
            resume = row[8]

            # Type de fichier ===============================
            type_fichier_str = row[10].strip()
            if type_fichier_str == "PDF":
                type_fichier_id = 1
            elif type_fichier_str == "VIDEO":
                type_fichier_id = 2
            else:
                # Gérer le cas où le type de fichier n'est pas valide
                raise ValueError("Le type de fichier n'est pas valide")

            # Lien vers le serveur ==========================
            lien_serveur = row[11].strip()
            if not lien_serveur :
                raise ValueError("Indiquez le chemin montrant l'emplacement du document")
            if os.path.exists(lien_serveur):
                pass
            else :
                raise ValueError("le fichier n'existe pas encore dans ce repertoire", lien_serveur)
            # Créez une instance de la classe Language correspondant à la langue du livre
            langue = Langue.objects.get(id=langue_id)

            # Créez une instance de la classe FileType correspondant au type de fichier du livre
            type_fichier = Type.objects.get(id=type_fichier_id)

            # Créez une instance de la classe Book et sauvegardez-la dans la base de données


            book = Book(id=id_tohiny, code_projet=code_projet, title=titre, langue=langue, publication_date=date_pub,
                        descripteur_matieres=descripteur,
                        auteur=auteur, niveau_bibliographique=niveau_biblio, thématique=thematique, résumé=resume,
                        type=type_fichier, lien=lien_serveur, utilisateur_resp_id=logged_user.id)
            book.save()
            id_tohiny += 1

        # Soratana anaty 'e' amin'izay izay value error azo tany aloha
        except ValueError as e:
            # Gérer l'erreur
            Message = f"Erreur lors de la lecture de la ligne {compteur}: {str(e)}"
            print(Message)
            # Arrêter le traitement
            return ["ERREUR_CSV", Message ]
            break

        except Exception as e:
            # Gérer les autres erreurs
            print(f"Erreur inattendue lors de la lecture de la ligne {compteur}: {str(e)}")
            # Continuer le traitement avec la ligne suivante
            continue
        compteur += 1
def confirmation(request):
    return render(request, 'confirmation.html')

# Fonction de visualisation des fichiers
def view_file(request, chemin):
    from django.http import HttpResponse, Http404
    import os

    # Chemin d'accès complet au fichier PDF
    file_path = chemin

    # Vérifie si le fichier existe et est lisible

    file_name = os.path.basename(file_path)
    print("FILENAAAAAAAAAAAAAAAAAAAAAAAAAAME", file_name)

    if file_name:
        content_type = mimetypes.guess_type(file_path)[0]
        print("content tyyyype", content_type)
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