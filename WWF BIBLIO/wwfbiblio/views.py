import mimetypes
import os

from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect
from reviews.models import Book
from account.views import get_logged_user_id
from reviews.views import recherche, recherche_brute


# C'EST LA VUE DES RESULTATS DE RECHERCHE ET PAGE D'ACCEUIL (url = /welcome)
def welcome(request):
    # FANALANA ESPACE AMIN'NY TITRE ===================
    #Boky = Book.objects.all()
    #for i in Boky:
        #i.title = i.title.strip()
        #i.save()
    logged_user = get_logged_user_id(request)
    if logged_user:
    # =================================================

        if len(request.GET) > 0 :

    # Gestion de l'onglet actif du templates. ===========================================
            if request.GET.get("pageAll"):
                active_tab = "tab1"
            elif request.GET.get("pageCP"):
                active_tab = "tab2"
            elif request.GET.get("pageTheme"):
                active_tab = "tab3"
            elif request.GET.get("pageAnnee"):
                active_tab = "tab4"
            else:
                active_tab = None

            if active_tab is None:
                active_tab = 'tab1'
        # ============================================================================


        # RECHERCHE ET TRIAGE PAR ORDRE DE RECHERCHE =================================
            # Utilisation de la fonction recherche
            champ_recherche = request.GET["recherche"].strip() # Suppression des espace en avant et en arriere
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
            cp_result = resultat[1] # Ilay fonction recherche()

            # Alaina daholo ny cp an'ireo objet
            liste_cp = []
            for objet in cp_result:
                if objet.code_projet not in liste_cp :
                    if "|" in objet.code_projet:
                        cp_misaraka = objet.code_projet.split("|")
                        for item in cp_misaraka:
                            if item in liste_cp:
                                pass
                            else:
                                liste_cp.append(item)
                    else :
                        liste_cp.append(objet.code_projet)
                else :
                    pass

            # Diovina kely ilay cp sao misy espace avant na apres
            LISTE_cp = []
            for cp in liste_cp:
                Espace_avant_apres = cp.strip() # manala espace supplementaire avant et apres
                #if " " in Espace_avant_apres:
                    #Espace_avant_apres = Espace_avant_apres.replace(" ", "")
                LISTE_cp.append(Espace_avant_apres)
            print("liste cp", LISTE_cp)

            # Alaina ny cp 6 caracteres mba hi creer-na dossier
            CP_vaovao=[]

            for CP in LISTE_cp :

                if "." in CP :
                    index = CP.find(".")
                    s = ''.join(CP[x] for x in range(len(CP)) if x < index)
                    if s not in CP_vaovao:
                        CP_vaovao.append(s)
                    else:
                        pass
                else :
                    if len(CP) == 8 :
                        s = ''.join(CP[x] for x in range(len(CP)) if x < 6)
                        if s not in CP_vaovao:
                            CP_vaovao.append(s)
                        else:
                            pass

                    elif len(CP) < 8 :
                        if CP not in CP_vaovao:
                            CP_vaovao.append(CP)
                        else:
                            pass
                    else :
                        if CP not in CP_vaovao:
                            CP_vaovao.append(CP)
                        else:
                            pass

            # Iny CP_vaovao iny no entina miditra ao amin'ny pagination django

            Objet_by_cp = sorted(CP_vaovao, key = lambda x: int(x[2:])) # Triage alphabetique
            final_cp = Objet_by_cp  # CP final no ampiasaiko satria tsy ampiasa pagination aho
                                    # (sao mbola hiverina ampiasa dia tsy tiako kitihina ilay Objet_by_cp )
            print("Objet_by_cp", Objet_by_cp)
            NOMBRE_DE_LIVRE_PAP_cp = []
            for item in Objet_by_cp:
                livre = Book.objects.filter(code_projet__icontains=item)
                nombredulivre = len(livre)
                NOMBRE_DE_LIVRE_PAP_cp.append(nombredulivre)

            # Chaque page est composé d'au plus 10 objets
            p_cp = Paginator(Objet_by_cp, 10) # tsy nampiasaina ity pagination ity ho an'ny CP

            # Prendre le numero de page envoyé via template
            page_number = request.GET.get("pageCP")

            # Prendre les objets correspondant au numero de page envoyé via template
            page_obj_by_cp = p_cp.get_page(page_number)


            # =====================TAPITRA ETO NY THEME MISY PAGINATION==============


# THEME (tsy misy pagination ito manaraka ito) =======================================
            # Alaina ny thematique rehetra

            theme_des_objets = []
            for i in resultat[2]:
                theme_des_objets.append(i.thématique)
            list_theme = []
            for i in theme_des_objets:
                # alaina ny theme rehetra raha misy boky manana theme maromaro (nampiasa | i ranja)
                if "|" in i :
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
                    else :
                        list_theme.append(i_sans_espace)
            print("list theme :", list_theme)
            NOMBRE_DE_LIVRE_PAP_th = []
            for item in list_theme:
                livre = Book.objects.filter(thématique__icontains=item)
                nbr_livre_th = len(livre)
                NOMBRE_DE_LIVRE_PAP_th.append(nbr_livre_th)
            print("nbr par theme :", NOMBRE_DE_LIVRE_PAP_th)
            # if not list_theme: azo tester-na toa izao iny liste raha vide na tsia


# ANNEE =================================================================

            list_Annee = []
            for book in resultat[4]:
                annee = book.publication_date
                if annee not in list_Annee and type(annee) is int:
                    list_Annee.append(annee)
                else:
                    pass

            list_Annee.sort()  # Tsy atao anaty variable rehefa mampiasa methode Sort() ex = a.sort() (tsy mety)
            NOMBRE_DE_LIVRE_PAP_annee = []

            for item in list_Annee:
                livre = Book.objects.filter(publication_date__icontains=item)
                nbr_livre_annee = len(livre)
                NOMBRE_DE_LIVRE_PAP_annee.append(nbr_livre_annee)

# Sortie vers le template :==========================================================
            #if page_obj_by_title: # Misy page obj ve? tsy misy io raha vide ilay resultat[0] avy @ recherche
                #print("obj_be title", page_obj_by_title)
            #else:
                #print(Objet_by_title)
                #print("tsisy")
            # raha vide ilay objet avy any amin'ny fonction recherche ka manao if page_obj_by_title dia
                # lasa mankany amin'ny else izy (io ambony anaty if io ny test nataoko)

            CONTEXT = {#"page_obj_by_CP": page_obj_by_cp,
                        #"page_obj_by_title" : page_obj_by_title,
                        #"page_obj_by_theme" : page_obj_by_theme,
                        "page_obj_by_all" : page_obj_by_all,
                        "active_tab" : active_tab,
                        "recherche": request.GET["recherche"],}

            if logged_user.is_admin == True:
                CONTEXT["logged_user_is_admin" ] =  "True"
            if len(final_cp) != 0 and len(NOMBRE_DE_LIVRE_PAP_cp) !=0 :
                # Atao anaty ny liste roa raha te hampiasa azy miaraka anaty boucle de template
                CONTEXT["ZIP_CP"] = zip( final_cp, NOMBRE_DE_LIVRE_PAP_cp)
            if len(list_theme) != 0 and len(NOMBRE_DE_LIVRE_PAP_th) !=0 :
                CONTEXT["ZIP_TH"] = zip(list_theme, NOMBRE_DE_LIVRE_PAP_th)
            if len(list_Annee) != 0 and len(NOMBRE_DE_LIVRE_PAP_annee) !=0 :
                CONTEXT["ZIP_AN"] = zip(list_Annee, NOMBRE_DE_LIVRE_PAP_annee)
            return render(request, "result_filtre.html", CONTEXT)




        else:
            trois_dernier_id = Book.objects.order_by('-id')[:3]
            trois_dernier_book = Book.objects.filter(id__in=trois_dernier_id)
            print("tsy nahita")
            return render(request, "base.html", {'trois_der_book' : trois_dernier_book})
    else:
        return redirect('/accounts/login')

# Views pour l'affichage de tous les documents (lien DOCUMENTS)
def tous_les_documents(request):
    logged_user = get_logged_user_id(request)
    if logged_user :
        if request.GET.get("Titre"):
            active_tab = "tab1"
        elif request.GET.get("CP"):
            active_tab = "tab2"
        elif request.GET.get("Theme"):
            active_tab = "tab3"
        elif request.GET.get("Annee"):
            active_tab = "tab4"
        else:
            active_tab = None

        if active_tab is None:
            active_tab = 'tab1'


        boky = Book.objects.all()

        # tous les titre ===================================================================================================
        title =[]
        ID = []
        boky_alphabetique = Book.objects.order_by('title') # alphabetique
        for book in boky_alphabetique:
            title.append(book.title.strip())
            ID.append(book.id)

        #tous les CP =======================================================================================================
        liste_cp = []
        for objet in boky: # Boky io efa declaré ao ambony ao (tous les documents)
            if objet.code_projet :
                if objet.code_projet not in liste_cp:
                    if "|" in objet.code_projet:
                        cp_misaraka = objet.code_projet.split("|")
                        print("cp_misaraka", cp_misaraka)
                        for item in cp_misaraka:
                            if item in liste_cp:
                                pass
                            else:
                                liste_cp.append(item)
                    else:
                        liste_cp.append(objet.code_projet)
                else:
                    pass
            else:
                pass

        # Diovina kely ilay cp sao misy espace avant na apres
        LISTE_cp = []
        for cp in liste_cp:
            Espace_avant_apres = cp.strip()  # manala espace supplementaire avant et apres
            # if " " in Espace_avant_apres:
            # Espace_avant_apres = Espace_avant_apres.replace(" ", "")
            LISTE_cp.append(Espace_avant_apres)


        # Alaina ny cp 6 caracteres mba hi creer-na dossier
        CP_vaovao = []
        for CP in LISTE_cp:

            if "." in CP:
                index = CP.find(".")
                s = ''.join(CP[x] for x in range(len(CP)) if x < index)
                if s not in CP_vaovao:
                    CP_vaovao.append(s)
                else:
                    pass

            else:
                if len(CP) == 8:
                    s = ''.join(CP[x] for x in range(len(CP)) if x < 6)
                    if s not in CP_vaovao:
                        CP_vaovao.append(s)
                    else:
                        pass
                elif len(CP) < 8:
                    if CP not in CP_vaovao:
                        CP_vaovao.append(CP)
                    else:
                        pass
                else:
                    if CP not in CP_vaovao:
                        CP_vaovao.append(CP)
                    else:
                        pass

        karazana_cp_hafa = []
        for cp in CP_vaovao:
            if cp[:2] == "MG":
                pass
            else :
                CP_vaovao.remove(cp)
                karazana_cp_hafa.append(cp)
        CP_triE = sorted(CP_vaovao, key=lambda x: int(x[2:]))  # Triage alphabetique

        # Averina anaty liste CP ihany ny CP trié
        for cp in karazana_cp_hafa:
            CP_triE.append(cp)

        print("cp triE", CP_triE)

        NOMBRE_DE_LIVRE_PAP_cp = []
        for item in CP_triE:
            livre = Book.objects.filter(code_projet__icontains=item)
            nombredulivre = len(livre)
            NOMBRE_DE_LIVRE_PAP_cp.append(nombredulivre)

        # Liste de tous les themes =========================================================================================
        themes = []
        for i in boky:
            if i.thématique:
                themes.append(i.thématique)
            else:
                pass
        print("THEME", themes)
        list_theme = []
        for i in themes:
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

        Liste_theme = sorted(list_theme)
        NOMBRE_DE_LIVRE_PAP_th = []

        print(type(Liste_theme))

        for item in Liste_theme:
            livre = Book.objects.filter(thématique__icontains=item)
            nbr_livre_th = len(livre)
            NOMBRE_DE_LIVRE_PAP_th.append(nbr_livre_th)

        # Liste de tous les années =========================================================================================

        Annee = []
        for book in boky:
            annee = book.publication_date
            if annee not in Annee and type(annee) is int:
                Annee.append(annee)
            else:
                pass

        Annee.sort() # Tsy atao anaty variable rehefa mampiasa methode Sort() ex = a.sort() (tsy mety)
        NOMBRE_DE_LIVRE_PAP_annee = []

        for item in Annee:
            livre = Book.objects.filter(publication_date__icontains=item)
            nbr_livre_annee = len(livre)
            NOMBRE_DE_LIVRE_PAP_annee.append(nbr_livre_annee)


        return render(request, "tous_les_documents.html", {"Zip_title" : zip(title,ID),
                                                           "Zip_CP_triE" : zip(CP_triE, NOMBRE_DE_LIVRE_PAP_cp),
                                                           "Zip_theme" : zip(Liste_theme, NOMBRE_DE_LIVRE_PAP_th),
                                                           "Zip_annee" : zip(Annee, NOMBRE_DE_LIVRE_PAP_annee),
                                                           "active_tab" : active_tab})
    else :
        return redirect("/login")

# mampiseho repertoire
def get_chemin_repertoire(contexte):
    return contexte['chemin_repertoire']

def showrepertoire(request):
    import subprocess
    chemin_fichier = r"E:\BUREAU\EAMAC1.png"
    subprocess.Popen(r'explorer /select,"{}"'.format(chemin_fichier))
    return None

def download_batch_file(request, chemin, titre):
    # Chemin vers le fichier à ouvrir
    chemin_fichier = chemin

    if chemin_fichier == "None":
        return HttpResponse("Le fichier n'est pas dans la disque dure", status=400)

    # Créer le contenu du fichier batch
    contenu_batch = '@echo off\nexplorer /select,"{}"'.format(chemin_fichier)

    # Nom du fichier batch à créer
    nom_fichier = '{}.bat'.format(titre)

    # Écrire le contenu dans le fichier batch
    with open(nom_fichier, 'w') as f:
        f.write(contenu_batch)

    # Ouvrir le fichier batch en tant que réponse HTTP
    with open(nom_fichier, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(nom_fichier)

    # Supprimer le fichier batch
    os.remove(nom_fichier)
    return response

# Ito ilay fontion utilisé rehefa avy miclic dossier iray ao anaty CP, na Année, na ny toa izany
def cp_th_ann(request):
    if request.GET.get("CP"):
        Boky = Book.objects.filter(code_projet__icontains = request.GET["CP"])
        return render(request, "result_apres_filtre.html", {"boky" : Boky , "page_demandE" : "CP"})
    elif request.GET.get("theme") :
        Boky = Book.objects.filter(thématique__icontains = request.GET["theme"])
        return render(request, "result_apres_filtre.html", {"boky": Boky , "page_demandE" : "theme"})
    elif request.GET.get("Annee") :
        Boky = Book.objects.filter(publication_date__icontains=request.GET["Annee"])
        return render(request, "result_apres_filtre.html", {"boky": Boky , "page_demandE" : "date"})