# profils/serializers.py
from rest_framework import serializers
from .models import Administrateur, Professionnel, Competence, SouscriptionProf, Abonnement, Type


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = ['id_type', 'nom']

class AbonnementSerializer(serializers.ModelSerializer):
    type = TypeSerializer(read_only=True)
    class Meta:
        model = Abonnement
        fields = ['id_abonnement', 'nom', 'critere', 'plage', 'validite', 'type']

class SouscriptionProfSerializer(serializers.ModelSerializer):
    abonnement = AbonnementSerializer(read_only=True)
    professionnel = serializers.PrimaryKeyRelatedField(queryset=Professionnel.objects.all())
    class Meta:
        model = SouscriptionProf
        fields = ['id_souscription_prof', 'abonnement', 'professionnel', 'date']

class CompetenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competence
        fields = ['id_competence', 'nom', 'description']

class AdministrateurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Administrateur
        fields = ['id_administrateur', 'nom', 'email']



class AdministrateurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Administrateur
        fields = ['id', 'user', 'nom']

class ProfessionnelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professionnel
        fields = ['id', 'user', 'nom', 'prenom', 'telephone', 'annee_experience',
                  'portfolio_link', 'cv', 'domaine_expertise', 'disponibilites',
                  'niveau_etudes', 'reseau_sociaux', 'pays', 'ville',
                  'test_psychologique_passe', 'valide_par_admin']