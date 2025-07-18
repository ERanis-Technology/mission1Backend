from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

class Type(models.Model):
    id_type = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    class Meta:
        db_table = 'type'
    def __str__(self):
        return self.nom
    

class Pays(models.Model):
    nom = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nom

    class Meta:
        db_table = 'pays'


class Ville(models.Model):
    nom = models.CharField(max_length=100)
    pays = models.ForeignKey(Pays, on_delete=models.CASCADE, related_name='villes')

    def __str__(self):
        return f"{self.nom} ({self.pays.nom})"

    class Meta:
        db_table = 'ville'
        unique_together = ('nom', 'pays')


class Abonnement(models.Model):
    id_abonnement = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    critere = models.CharField(max_length=200)
    plage_validite = models.CharField(max_length=100)  # Renommé de 'plage'
    validite = models.CharField(max_length=100)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, db_column='id_type')
    class Meta:
        db_table = 'abonnement'
    def __str__(self):
        return self.nom

class Administrateur(models.Model):
    id_administrateur = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mdp = models.CharField(max_length=255)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.mdp and not self.mdp.startswith('pbkdf2_sha256$'):
            self.mdp = make_password(self.mdp)
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'administrateur'
    def __str__(self):
        return self.nom

class Entreprise(models.Model):
    id_entreprise = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    secteur = models.CharField(max_length=100)
    besoin = models.TextField()
    mdp = models.CharField(max_length=255)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.mdp and not self.mdp.startswith('pbkdf2_sha256$'):
            self.mdp = make_password(self.mdp)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom

class Professionnel(models.Model):
    EXPERIENCE_CHOICES = [
        ('0-1', '0 à 1 an'),
        ('1-3', '1 à 3 ans'),
        ('3-5', '3 à 5 ans'),
        ('5+', 'Plus de 5 ans'),
    ]

    DISPONIBILITE_CHOICES = [
        ('temps_plein', 'Temps plein'),
        ('temps_partiel', 'Temps partiel'),
    ]

    NIVEAUX_ETUDE = [
        ('aucun', "Aucun diplôme"),
        ('cep', "Certificat d'Études Primaires (CEP)"),
        ('bepc', "Brevet d'Études du Premier Cycle (BEPC)"),
        ('probatoire', "Probatoire"),
        ('baccalaureat', "Baccalauréat"),
        ('bts', "BTS"),
        ('licence', "Licence"),
        ('master', "Master"),
        ('doctorat', "Doctorat"),
        ('autre', "Autre"),
    ]


    id_professionnel = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    tel = models.CharField(max_length=12)
    mdp = models.CharField(max_length=255)
    portfolio = models.URLField(max_length=300,blank=True,null=True,verbose_name="Lien vers le portfolio")
    annee_experience = models.CharField(max_length=5,choices=EXPERIENCE_CHOICES,verbose_name="Années d'expérience")
    disponibilite = models.CharField(max_length=13,choices=DISPONIBILITE_CHOICES,default='temps_partiel',verbose_name="Disponibilité")
    niveau_d_etude = models.CharField(max_length=20,choices=NIVEAUX_ETUDE,default='aucun',verbose_name='Niveau d\'étude')
    photo = models.ImageField(upload_to='photos/professionnels/', blank=False, null=False)
    pays = models.ForeignKey(Pays, on_delete=models.SET_NULL, null=True, blank=True)
    ville = models.ForeignKey(Ville, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    score_performance = models.FloatField(default=0.0)
    autres_competences = models.CharField(max_length=255,default="Aucune")
    cv = models.FileField(upload_to='cvs/',verbose_name='CV (format PDF)')

    def save(self, *args, **kwargs):
        if self.mdp and not self.mdp.startswith('pbkdf2_sha256$'):
            self.mdp = make_password(self.mdp)
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'professionnel'
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

class Categorie(models.Model):
    nom = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nom

    class Meta:
        db_table = 'categorie'

class SousDomaine(models.Model):
    nom = models.CharField(max_length=100)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, related_name='sous_domaines')

    def __str__(self):
        return f"{self.nom} ({self.categorie.nom})"

    class Meta:
        db_table = 'sous_domaine'
        unique_together = ('nom', 'categorie')

class Competence(models.Model):
    id_competence = models.AutoField(primary_key=True)
    sous_domaine = models.ForeignKey(SousDomaine, on_delete=models.CASCADE, related_name='competences')
    description = models.TextField(blank=True)
    professionnel = models.ForeignKey(Professionnel, on_delete=models.CASCADE, related_name='competences')

    def __str__(self):
        return f"{self.sous_domaine.nom} ({self.sous_domaine.categorie.nom})"

    class Meta:
        db_table = 'competence'


class ReseauSocial(models.Model):
    professionnel = models.ForeignKey(
        'Professionnel',
        on_delete=models.CASCADE,
        related_name='reseaux_sociaux'
    )
    plateforme = models.CharField(
        max_length=50,
        choices=[
            ('facebook', 'Facebook'),
            ('twitter', 'Twitter'),
            ('instagram', 'Instagram'),
            ('linkedin', 'LinkedIn'),
            ('tiktok', 'TikTok'),
            ('github', 'GitHub'),
            ('autre', 'Autre'),
        ]
    )
    lien = models.URLField(max_length=300, verbose_name="Lien ou profil")

    def __str__(self):
        return f"{self.professionnel.nom} - {self.plateforme}"

