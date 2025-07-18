# profils/models.py
from django.db import models


class Entreprise(models.Model):
    id_entreprise = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    secteur = models.CharField(max_length=100)
    besoin = models.TextField()

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

class Administrateur(models.Model):
    id_administrateur = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    class Meta:
        db_table = 'administrateur'
    def __str__(self):
        return self.nom

class Professionnel(models.Model):
    id_professionnel = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
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

class Competence(models.Model):
    id_competence = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    professionnel = models.ForeignKey(Professionnel, on_delete=models.CASCADE, related_name='competences')
    class Meta:
        db_table = 'competence'
    def __str__(self):
        return self.nom