from django.contrib import auth
from django.db import models

class Book(models.Model):  # A published book.
    code_projet = models.CharField(max_length=1000, null=True, blank=True, verbose_name="Code projet")
    title = models.CharField(max_length=300, help_text="Titre du document.", verbose_name="Titre*", blank=False,null=True)
    langue = models.ForeignKey('Langue', null=True, on_delete=models.DO_NOTHING, verbose_name="Langue*")
    publication_date = models.IntegerField(verbose_name="Année de publication", null=True,blank=True )
    descripteur_matieres = models.CharField(max_length=1000, blank=True, null=True )
    auteur = models.CharField(max_length= 1000,  blank=True, null=True)
    niveau_bibliographique = models.CharField(max_length=1000, blank=True, null=True)
    thématique = models.CharField(max_length=20, null=True,  verbose_name="Thème*")
    résumé = models.TextField(max_length=5000, blank=True, null=True, verbose_name="Résumé/Description")
    type = models.ForeignKey('Type', null=True, on_delete=models.DO_NOTHING, verbose_name="Type *")
    lien = models.CharField(max_length=260, null=True, verbose_name="Lien vers le serveur*")



    # niveau du document
    MY_CHOICES = (
        (1, 'Niveau 1'),
        (2, 'Niveau 1 et niveau 2'),
        (3, 'Tout le monde')
    )
    niveau = models.IntegerField(choices=MY_CHOICES, null=True, verbose_name="Ce document sera accessible à un compte de quel niveau?")
    # id de l'utilisateur
    utilisateur_resp_id = models.IntegerField(null=True)
    lieu = models.ForeignKey('Lieu', null=True, on_delete=models.DO_NOTHING, verbose_name="Lieu")


    # Ce parametre through est destiné juste pour les relations n-n. C'est pour visé le nom d'un table
    # intermediaire (qui est egalement une class python) necessaire pour stocker des informations
    # supplementaire relié au deux tables "Contributor" et "Book" . Web dev page 97
    # Ici, cette information supplementaire est pour specifier le type de contributeur (est-ce un auteur? co-auteur ?
    # editeur?

    def __str__(self):
        return self.title

class Lieu(models.Model):
    lieu = models.CharField(max_length=60)
    def __str__(self):
        return self.lieu
class Langue(models.Model):
    langue = models.CharField(max_length=10)
    def __str__(self):
        return self.langue
class Type(models.Model):
    type = models.CharField(max_length=10)
    def __str__(self):
        return self.type
# Tsy misy ilako ny Review model io -----------------------------------------------------
class Review(models.Model): #PAGE 100
    content = models.TextField(help_text="The Review text.")
    rating = models.IntegerField(help_text="The rating the reviewer has given.")
    date_created = models.DateTimeField(auto_now_add=True, help_text= "The date and time the review was created.")
    date_edited = models.DateTimeField(null=True,  help_text="The date and time the review was last edited.")
    creator = models.ForeignKey(auth.get_user_model(), on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE,help_text="The Book that this review is for.")

class Contributor(models.Model):  # A contributor to a Book, e.g. author, editor,co-author
    first_names = models.CharField(max_length=50, help_text="The contributor's first name or names.")
    last_names = models.CharField(max_length=50, help_text="The contributor's last name or names.")
    email = models.EmailField(help_text="The contact email for the contributor.")

    def __str__(self):
        return self.first_names

# Page 97 Web dev with  Django (C'est juste une table intermediaire pour definir le type dde contributeur)
class BookContributor(models.Model):
    class ContributionRole(models.TextChoices):
        AUTHOR = "AUTHOR", "Author"
        CO_AUTHOR = "CO_AUTHOR", "Co-Author"
        EDITOR = "EDITOR", "Editor"

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    contributor = models.ForeignKey(Contributor, on_delete=models.CASCADE)
    role = models.CharField(verbose_name="The role this contributor had in the book.",
                            choices=ContributionRole.choices, max_length=20)
