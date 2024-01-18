import os

from django import forms
from django.contrib.auth import get_user_model
User = get_user_model()
from reviews.models import Book



class nouveaudocform(forms.ModelForm):
    #dossier = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}), required=False)
    fichier = forms.FileField()

    class Meta:

        model = Book
        fields = ['niveau',
                    'code_projet',
                    "title",
                    "langue",
                    "descripteur_matieres",
                    "niveau_bibliographique",
                    "publication_date",
                    "auteur",
                    "thématique",
                    "résumé",
                    "type",
                    "lien"]
        widgets = {
            'code_projet': forms.TextInput(attrs={'placeholder': 'MG...'}),
            'title': forms.TextInput(attrs={'placeholder': 'Titre du document...'}),
            'auteur' : forms.TextInput(attrs={'placeholder': 'Auteur 1 | Auteur 2 | ...'}),
            #'lien': forms.TextInput(attrs={'placeholder': 'Sélectionner un dossier...', 'readonly': 'readonly'})

        }
    '''
    vao passé ao anaty vu ny request.GET na request.POST (form = nouveaudoc(request.POST)) 
    dia efa traité ireto fonctio clean ireto. 
    Donc raha tsy valide ny formulaire ka mipasse any amin'ny else (contraire de if form.is_valid()) dia 
    passer-na any amin'ilay form vaovao ny parametre request.POST ka efa voavaky sahady ireto..
    
    Raha tsy tafiditra izany ny request.POST (na GET), dia miretourne None ny champs rehetra. Toy ny champs mbola
    tsy nofenoina. Valable toa izany koa ny request.FILES (Ca m'as pris un jour de l'avoir su en obtenant un nom 
    de fichier None au niveau du champs fichier)
    '''
    def clean(self):
        cleaned_data = super().clean()
        fichier = cleaned_data.get('fichier')
        lien = cleaned_data.get('lien')

        CP = cleaned_data.get('code_projet')
        print(lien, fichier)

        if fichier and lien:

            # Créer le chemin complet du fichier
            filename = os.path.join(lien, fichier.name)

            if os.path.exists(filename):
                # tSY MIPOITRA RAHA TSY TAFIDITRA EN PARAMETRE ANY AMIN'NY VUE NY request.FILES
                self.add_error("fichier", "Un fichier de même nom existe déjà dans ce répértoire...")

            else :
                pass
        import re
        if CP :
            cp = CP.strip()
            if "|" in cp :
                cp_misaraka = cp.split("|")
                for cp in cp_misaraka:
                    cp1=cp.strip()
                    if re.search(r'\s', cp1):
                        self.add_error("code_projet", "Le code projet ne doit pas contenir d'espaces")
            else:
                if re.search(r'\s', cp):
                    self.add_error("code_projet", "Le code projet ne doit pas contenir d'espaces")
        return cleaned_data

from django.core.exceptions import ValidationError
import csv
class form_csv(forms.Form):
    csv_file = forms.FileField(label='Choisissez un fichier CSV')

    def clean_csv_file(self):
        csv_file = self.cleaned_data['csv_file']
        content_type = csv_file.content_type

        if content_type != 'text/csv':
            raise ValidationError('Le fichier doit être un fichier CSV.')
        try:
            csv_reader = csv.reader(csv_file)
        except Exception as e:
            raise ValidationError(f"Impossible de lire le fichier CSV: {e}")

        return csv_file