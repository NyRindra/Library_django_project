from django import forms
from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model
User = get_user_model()


class LoginForm(forms.Form):
    email = forms.EmailField(label='Courriel', widget=forms.EmailInput(attrs={'placeholder': 'Adresse email'}))
    password = forms.CharField(label='Mot de passe', widget=forms.PasswordInput(attrs={'placeholder': 'Mot de passe'}))

    def clean(self):  #(PAGE 233)
        cleaned_data = super(LoginForm, self).clean()  # ito super ito no niantso an'ilay clean ka natao
        # tanaty variable "clean_data" izy vao nampiasaina (DICTIONNAIRE NY CLEANED_DATA)
        _email = cleaned_data.get("email")  # Natao ato anaty variable "_email" ilay email azo tao amin'ny request.POST
        _password = cleaned_data.get("password")  # On a fait de meme pour le password se trouvant dans request.POST
        # print("nandalo test")
        # print(_email)  # test fotsiny
        # print(cleaned_data) : C'est un dictionnaire comme {'email': 'ny.rindra.rk@gmail.com', 'password': '1234578'}
        # VERIFICATION DES DEUX CHAMPS
        # a- Raha validé tao amin'ny formulaire ilay mdp sy courriel, izany hoe voamarina fa tsy vide na adresse mazava
        if _email and _password:  # raha misy ilay _email sy _password, izany hoe tsy "None"
            # EXPLICATION PAGE 259
            result = User.objects.filter(email=_email)
            if len(result) == 1 :
                logged_user = User.objects.get(email=_email)

                # verifiction de mot de passe hashé...
                if check_password(_password, logged_user.password) :
                    pass
                else :
                    raise forms.ValidationError("Identifiant ou Mot de passe erroné.")
            else:
                raise forms.ValidationError("Identifiant ou Mot de passe erroné.")


# ====================================================================================================================


from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import User
User = get_user_model()

class RegisterForm(forms.ModelForm):
    """
    The default
    """
    password = forms.CharField(widget=forms.PasswordInput) # Champ qui ne decoule pas du modele
    password_2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['nom', 'prénom', 'email'] # Champ qui decoule du modele

    #ireto fonction manaraka ireto no tsy takatry ny is_valid() :
        # Tsy maintsy jerena hoe efa misy ve ny email
        # Conforme ve ny password sy ny confirm password
    def clean_email(self):
        '''
        Verify email is available.
        '''
        # Cleaned_data.get dia azo ampiasaina maina raha anaty modele ilay champ (io ambany misy ex raha tsy anaty modele)
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("l'e-mail est pris")
        return email

    def clean(self):
        '''
        Vérifiez que les deux mots de passe correspondent.
        '''
        # Tsy maintsy antsoina avy any amin'ny super ny cleaned data tsy anaty modele ny champ
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")
        if password is not None and password != password_2:
            self.add_error("password_2", "Les deux mots de passes doivent être identiques")
        return cleaned_data

# Ito ny formulaire miasa amin'ity BIBLIO ity raha resaka creation de compte
class UserAdminCreationForm(forms.ModelForm):
    """
    Un formulaire pour créer de nouveaux utilisateurs. Comprend tout le nécessaire
    champs, plus un mot de passe répété.
    """
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Mot de passe'}))
    password_2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'placeholder': 'Confirmation'}))
    class Meta:
        model = User
        fields = ['nom', 'prénom', 'email']

        # Vao nampidirina taty aoriana ito widget ito fa tsy misy hidiran'ireo creation d'user ireo d'origine
        widgets = {
            'nom': forms.TextInput(attrs={'placeholder': 'Nom'}),
            'prénom': forms.TextInput(attrs={'placeholder': 'Prénom'}),
            'email': forms.TextInput(attrs={'placeholder': 'Adresse email'}),
        }

    def clean_email(self):
        '''
        Verify email is available.
        '''
        # Cleaned_data.get dia azo ampiasaina maina raha hi retourner ny données d'ensemble eo amin'ilay formulaire (données rehetra)
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("l'e-mail est pris")
        return email

    def clean(self):
        '''
        Vérifiez que les deux mots de passe correspondent.
        '''
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")
        if password is not None and password != password_2:
            self.add_error("password_2", "Mots de passes non identiques")
        return cleaned_data

    def save(self, commit=True):
        # Enregistrez le mot de passe fourni au format haché
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

# tsy azo fafaina fa ilaina ao amin'ny admin (Ca semble un peu inutile, voilà pourquoi il faut faire attention)
class UserAdminChangeForm(forms.ModelForm):
    """Un formulaire pour mettre à jour les utilisateurs. Inclut tous les champs sur
    l'utilisateur, mais remplace le champ du mot de passe par celui de l'administrateur
    champ d'affichage du hachage du mot de passe.
    """
    password = ReadOnlyPasswordHashField()
    class Meta:
        model = User
        fields = ['nom', 'prénom', 'email', 'password', 'is_active', 'admin']
        def clean_password(self):
            # Indépendamment de ce que l'utilisateur fournit, renvoie la valeur initiale.
            # Cela se fait ici, plutôt que sur le terrain, car le
            # le champ n'a pas accès à la valeur initiale
            return self.initial["password"]