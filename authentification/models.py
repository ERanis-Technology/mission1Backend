from django.db import models

# Create your models here.
class Entreprise(models.Model):

    id_entreprise = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    email = models.EmailField(unique=True, max_length=100)
    pwd = models.CharField(max_length=255)
    secteur = models.CharField(max_length=100)
    besoin = models.TextField()

    def __str__(self):
        return self.nom

class Adminitrateur(models.Model):

    id_administrateur = models.AutoField(primary_key=True) 
    nom = models.CharField(max_length=100)
    email = models.EmailField(unique=True, max_length=100)
    pwd = models.CharField(max_length=255)
    
    def __str__(self):
        return self.nom
    
class Professionnel(models.Model):

    id_professionnel = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    email = models.EmailField(unique=True, max_length=100)
    pwd = models.CharField(max_length=255)

    def __str__(self):
        return self.nom
     
    