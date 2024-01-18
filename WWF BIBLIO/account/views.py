from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm, UserAdminCreationForm
from .models import Person, userniv1, userniv2, userniv3
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from django.contrib.auth import get_user_model
User = get_user_model()

def log(request):
    # 1- Formulaire non vide
    if len(request.POST) > 0:
        formulaire = LoginForm(request.POST)

        # Formulaire valide
        if formulaire.is_valid():
            user_email = formulaire.cleaned_data['email']
            active_person = User.objects.get(email=user_email)
            request.session['logged_user_id'] = active_person.id  # Useful for looking at the online person
            return redirect("/welcome")

        # Formulaire non valide
        else:
            logged_user = get_logged_user_id(request)
            if logged_user:
                request.session.set_expiry(1)
            # retourne l'erreur de la fonction clean dans le formulaire (Ce qui n'est pas considéré par is_valid)
            formulaire = LoginForm(request.POST)
            context = {"formulaire": formulaire}
            return render(request, "login.html", context)

    # 2- Formulaire vide
    else:
        logged_user = get_logged_user_id(request)
        if logged_user:
            request.session.set_expiry(1)
        formulaire = LoginForm()
        context = {"formulaire": formulaire}
        return render(request, "login.html", context)



def voirmail(request):
    return render(request, "mailenvoyé.html")

# ================================= Utilisation d'un modele Django personnalisé =======================================

def nouveauCompte(request):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    # Formulaire non vide avec un element "AccountType" dans le dictionnaire request.GET
    if len(request.GET) > 0 and 'AccountType' in request.GET:
        formNIV1 = UserAdminCreationForm(request.GET, prefix='NV1')
        formNIV2 = UserAdminCreationForm(request.GET, prefix='NV2')
        formNIV3 = UserAdminCreationForm(request.GET, prefix='NV3')

        # Regarder si le type de compte demandé est de niveau 1
        if request.GET["AccountType"] == 'NIV1':
            if formNIV1.is_valid():
                email = formNIV1.cleaned_data["email"]
                password = formNIV1.cleaned_data["password"]

                # Creation de nouvel utilisateur (fonction create_superuser )
                New_user = User.objects.create_niveau1(email,password)
                return redirect('/accounts/login')
            else:
                formNIV1 = UserAdminCreationForm(request.GET,prefix='NV1')
                formNIV2 = UserAdminCreationForm(prefix='NV2')
                formNIV3 = UserAdminCreationForm(prefix='NV3')
                return render(request, 'signin.html',
                              {'form1': formNIV1, 'form2': formNIV2, 'form3': formNIV3})

        # Regarder si le type de compte demandé est de niveau 2
        elif request.GET["AccountType"] == 'NIV2':
            if formNIV2.is_valid():
                # formNIV2.save() Tsy ito intsony no nampiasaina fa no creer-na maina be ilay utilisateur
                email = formNIV2.cleaned_data["email"]
                password = formNIV2.cleaned_data["password"]

                # On cree donc un utilisateur via create_staffuser ==> trouvé dans le model (UserManager)
                New_user = User.objects.create_niveau2(email, password)
                return redirect('/accounts/login')
            else:
                formNIV1 = UserAdminCreationForm(prefix='NV1')
                formNIV2 = UserAdminCreationForm(request.GET,prefix='NV2')
                formNIV3 = UserAdminCreationForm(prefix='NV3')
                return render(request, 'signin.html', {'form1' : formNIV1, 'form2' : formNIV2, 'form3' : formNIV3 })

        # Regarder si le type de compte demandé est de niveau 3
        elif request.GET["AccountType"] == 'NIV3':
            if formNIV3.is_valid():
                # On sauvegarde seulement de formulaire (sady tsy staff no tsy admin raha ito fotsiny ny methode)
                formNIV3.save()
                return redirect('/accounts/login')
            else:
                formNIV1 = UserAdminCreationForm(prefix='NV1')
                formNIV2 = UserAdminCreationForm(prefix='NV2')
                formNIV3 = UserAdminCreationForm(request.GET,prefix='NV3')
                return render(request, 'signin.html', {'form1' : formNIV1, 'form2' : formNIV2, 'form3' : formNIV3 })

    else:
        print(request.GET)
        formNIV1 = UserAdminCreationForm(prefix='NV1')
        formNIV2 = UserAdminCreationForm(prefix='NV2')
        formNIV3 = UserAdminCreationForm(prefix='NV3')
        return render(request, 'signin.html', {'form1' : formNIV1, 'form2' : formNIV2, 'form3' : formNIV3 })

# =============================FIN tilisation d'un modele Django personnalisé =======================================

def get_logged_user_id(request):

    if 'logged_user_id' in request.session:  # 'logged_user' is what we've put in the request.session wile login
        logged_user_id = request.session['logged_user_id']
        if len(User.objects.filter(
                id=logged_user_id)) == 1:
            return User.objects.get(id=logged_user_id)  # Miretourner objet ilay fonction
        else:
            return None
    else:
        return None
