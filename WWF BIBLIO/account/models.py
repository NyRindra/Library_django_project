from django.db import models

class Person(models.Model):  # Creation d'une classe heritant la classe Model
    # On defini ensuite tous nos champs en specifiant leur types (Comme lors de la creation des formulaires
    nom = models.CharField(max_length=30)
    prénom = models.CharField(max_length=30)
    email = models.EmailField()
    mot_de_passe = models.CharField(max_length=32)  # dans le cas reel, nous ne devons pas stocker le mdp en clair
    confirmation = models.CharField(null=True ,max_length=32)

    person_type = 'generic' # Ohatra: Nampiasaina any amin'ny templates welcome ito

    def __str__(self):
        return self.nom + ' ' + self.prénom

# --------------------------Modele heritant la classe Person, donc ce sont des personnes...-----------------------------
class userniv1(Person):   # personne ihany fa classe fille fotsiny
    identifiant_niveau_1 = models.CharField(max_length=15)
    person_type = 'userniv1'


class userniv2(Person):   # personne ihany fa classe fille fotsiny
    identifiant_niveau_2 = models.CharField(max_length=15)
    person_type = 'userniv2'


class userniv3(Person):  # personne ihany koa fa classe fille fotsiny
    identifiant_niveau_3= models.CharField(max_length=15)
    person_type = 'userniv3'
    # -------------attribut statique------------


class fileupload(models.Model):
    fichier = models.FileField()


# =============================Utilisation d'un modele Django personnalisé=======================================
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

# Cette classe est en liaison avec la classe User, elle est mis comme variable "objects" dans la classe User
class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Crée et enregistre un utilisateur avec l'e-mail et le mot de passe donnés.
        """
        if not email:
            raise ValueError('Les utilisateurs doivent avoir une adresse e-mail')

        user = self.model(
        email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Crée et enregistre un utilisateur du staff avec l'e-mail et le mot de passe donnés.
        """
        user = self.create_user(email,password=password,)
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Crée et enregistre un superutilisateur avec l'e-mail et le mot de passe donnés.
        """
        user = self.create_user(email,password=password,)

        #Condition requise pour etre un admin
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user

    # Manomboka eto dia efa methode ampiasaiko manokana... Azo fafaina amin'ny projet hafa
    def create_niveau1(self, email, password):
        """
        Crée et enregistre un superutilisateur avec l'e-mail et le mot de passe donnés.
        """
        user = self.create_user(email,password=password,)

        #Condition requise pour etre un admin
        user.niveau_1 = True
        user.save(using=self._db)
        return user
    def create_niveau2(self, email, password):
        """
        Crée et enregistre un superutilisateur avec l'e-mail et le mot de passe donnés.
        """
        user = self.create_user(email,password=password,)

        #Condition requise pour etre un admin
        user.niveau_2 = True
        user.save(using=self._db)
        return user

    def admin_doc(self, email, password):
        """
        Crée et enregistre un superutilisateur avec l'e-mail et le mot de passe donnés.
        """
        user = self.create_user(email,password=password,)

        #Condition requise pour etre un admin
        user.admin_doc = True
        user.save(using=self._db)
        return user

# Utile pour la creation des formulaires
class User(AbstractBaseUser):
    objects = UserManager()  # ahafahana manao opperation CRUD toa ilay appel User.objects.all()
    email = models.EmailField(
        verbose_name='email adress',
        max_length=255,
        unique=True,error_messages={'blank': 'Ce champ est obligatoire.'}
    )
    nom = models.CharField(max_length=30, null=True, error_messages={'blank': 'Ce champ est obligatoire.'})
    prénom = models.CharField(max_length=30, null=True, error_messages={'blank': 'Ce champ est obligatoire.'})

    is_active = models.BooleanField(default=True) # L'utilisateur ne peut pas login sur django admin si c'est FALSE
    staff = models.BooleanField(default=False) # a admin user; non super-user
    admin = models.BooleanField(default=False) # a superuser

    admin_doc = models.BooleanField(default=False) # mi-gerer ny document
    niveau_1 = models.BooleanField(default=False)
    niveau_2 = models.BooleanField(default=False)
    # remarquez l'absence du "champ password", c'est intégré pas besoin de preciser.
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # Email & Password sont requis par défaut.
    def get_full_name(self):
        # L'utilisateur est identifié par son adresse e-mail
        return self.email
    def get_short_name(self):
        # L'utilisateur est identifié par son adresse e-mail
        return self.email
    def __str__(self):
        return self.email
    def has_perm(self, perm, obj=None):
        "L'utilisateur a-t-il une autorisation spécifique ?"
        # Réponse la plus simple possible : Oui, toujours
        return True
    def has_module_perms(self, app_label):
        "L'utilisateur dispose-t-il des autorisations nécessaires pour voir l'application ?`app_label`?"
        # Réponse la plus simple possible : Oui, toujours
        return True
    @property
    def is_staff(self):
        "L'utilisateur est-il un membre du personnel ?"
        return self.staff
    @property
    def is_admin(self):
        "L'utilisateur est-il un membre administrateur?"
        return self.admin

# =========================== FIN Utilisation d'un modele Django personnalisé ==========================================