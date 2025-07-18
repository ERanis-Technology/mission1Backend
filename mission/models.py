from django.db import models
from profils.models import 
# Create your models here.
class Mission(models.Model):
    STATUS_CHOICES = (
        ('EN_ATTENTE', 'En attente'),
        ('EN_COURS', 'En cours'),
        ('TERMINE', 'Terminé'),
    )

    id_mission = models.AutoField(primary_key=True)
    titre = models.CharField(max_length=200)
    description = models.TextField()
    entreprise = models.ForeignKey(User, on_delete=models.CASCADE, related_name='missions')  # Entreprise soumettant la mission
    administrateur = models.ForeignKey(Administrateur, on_delete=models.SET_NULL, null=True, related_name='missions_gerees')
    professionnel = models.ForeignKey(Professionnel, on_delete=models.SET_NULL, null=True, blank=True, related_name='missions')
    date_creation = models.DateTimeField(auto_now_add=True)
    date_debut = models.DateTimeField(null=True, blank=True)
    date_fin = models.DateTimeField(null=True, blank=True)
    statut = models.CharField(max_length=20, choices=STATUS_CHOICES, default='EN_ATTENTE')
    progression = models.IntegerField(default=0)  # Pourcentage de progression
    evaluation = models.FloatField(null=True, blank=True)  # Score d'évaluation

    def __str__(self):
        return self.titre