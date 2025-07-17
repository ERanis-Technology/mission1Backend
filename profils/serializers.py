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

class ProfessionnelSerializer(serializers.ModelSerializer):
    competences = CompetenceSerializer(many=True, read_only=True)
    souscriptions = SouscriptionProfSerializer(many=True, read_only=True, source='souscriptionprof_set')
    class Meta:
        model = Professionnel
        fields = ['id_professionnel', 'nom', 'email', 'competences', 'souscriptions']