from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.conf import settings

class CustomUserManager(BaseUserManager):
    def create_user(self, email, user_type, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, user_type=user_type, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, user_type, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, user_type, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_type']

    USER_TYPE_CHOICES = (
        ('admin', 'Administrateur'),
        ('prof', 'Professionnel'),
        ('ent', 'Entreprise'),
    )

    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Administrateur(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    nom = models.CharField(max_length=100)
    class Meta:
        db_table = 'administrateur'
    def __str__(self):
        return self.nom

class Professionnel(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    nom = models.CharField(max_length=100)
    class Meta:
        db_table = 'professionnel'
    def __str__(self):
        return self.nom

class Entreprise(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    nom = models.CharField(max_length=100)
    secteur = models.CharField(max_length=100)
    besoin = models.TextField()
    class Meta:
        db_table = 'entreprise'
    def __str__(self):
        return self.nom

class Type(models.Model):
    id_type = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    class Meta:
        db_table = 'type'
    def __str__(self):
        return self.nom

class Abonnement(models.Model):
    id_abonnement = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    critere = models.CharField(max_length=200)
    plage = models.CharField(max_length=100)
    validite = models.CharField(max_length=100)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, db_column='id_type')
    class Meta:
        db_table = 'abonnement'
    def __str__(self):
        return self.nom

class SouscriptionProf(models.Model):
    id_souscription_prof = models.AutoField(primary_key=True)
    abonnement = models.ForeignKey(Abonnement, on_delete=models.CASCADE, db_column='id_abonnement')
    professionnel = models.ForeignKey(Professionnel, on_delete=models.CASCADE, db_column='id_professionnel')
    date = models.DateField()
    class Meta:
        db_table = 'souscription_prof'
    def __str__(self):
        return f"{self.professionnel.nom} - {self.abonnement.nom}"

class Competence(models.Model):
    id_competence = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    professionnel = models.ForeignKey(Professionnel, on_delete=models.CASCADE, related_name='competences')
    class Meta:
        db_table = 'competence'
    def __str__(self):
        return self.nom