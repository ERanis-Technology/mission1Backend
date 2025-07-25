from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from profils.models import Administrateur, Entreprise, Professionnel, SousDomaine, Competence
from .utils import send_confirmation_email
import logging

logger = logging.getLogger(__name__)#Apres il faudra enlever ceci parce que ca affiche tous les journeaux

# Base serializer for common user fields
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return User.objects.create(**validated_data)

# Administrateur Registration Serializer
class AdministrateurRegistrationSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)

    class Meta:
        model = Administrateur
        fields = ['user', 'nom', 'email', 'mdp']

    def validate(self, data):
        user_data = data.get('user', {})
        user_data['username'] = data.get('nom', user_data.get('username', ''))
        user_data['email'] = data.get('email', user_data.get('email', ''))
        user_data['password'] = data.get('mdp', user_data.get('password', ''))
        data['user'] = user_data
        if not data['user']['username'] or not data['user']['email'] or not data['user']['password']:
            raise serializers.ValidationError("Les champs nom, email et mdp sont requis.")
        if Administrateur.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("Cet email est déjà utilisé.")
        return data

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer().create(user_data)
        validated_data['mdp'] = make_password(validated_data['mdp'])
        administrateur = Administrateur.objects.create(
            user=user,
            nom=validated_data['nom'],
            email=validated_data['email'],
            mdp=validated_data['mdp']
        )
        send_confirmation_email(administrateur.email, 'administrateur')
        return administrateur

# Entreprise Registration Serializer
class EntrepriseRegistrationSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)

    class Meta:
        model = Entreprise
        fields = ['user', 'nom', 'email', 'mdp', 'tel', 'secteur', 'besoin', 'nombre_employees',
                  'lien_site_web', 'adresse', 'logo', 'personne_de_contact', 'type_abonnement',
                  'moyen_paiement', 'acceptation_condition']

    def validate(self, data):
        user_data = data.get('user', {})
        user_data['username'] = data.get('nom', user_data.get('username', ''))
        user_data['email'] = data.get('email', user_data.get('email', ''))
        user_data['password'] = data.get('mdp', user_data.get('password', ''))
        data['user'] = user_data
        if not data['user']['username'] or not data['user']['email'] or not data['user']['password']:
            raise serializers.ValidationError("Les champs nom, email et mdp sont requis.")
        if Entreprise.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("Cet email est déjà utilisé.")
        return data

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer().create(user_data)
        validated_data['mdp'] = make_password(validated_data['mdp'])
        entreprise = Entreprise.objects.create(
            user=user,
            nom=validated_data['nom'],
            email=validated_data['email'],
            mdp=validated_data['mdp'],
            tel=validated_data['tel'],
            secteur=validated_data['secteur'],
            besoin=validated_data['besoin'],
            nombre_employees=validated_data.get('nombre_employees'),
            lien_site_web=validated_data.get('lien_site_web'),
            adresse=validated_data['adresse'],
            logo=validated_data['logo'],
            personne_de_contact=validated_data['personne_de_contact'],
            type_abonnement=validated_data['type_abonnement'],
            moyen_paiement=validated_data['moyen_paiement'],
            acceptation_condition=validated_data['acceptation_condition']
        )
        send_confirmation_email(entreprise.email, 'entreprise')
        return entreprise
# Login Serializer
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class ProfessionnelRegistrationSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    competences = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = Professionnel
        fields = [
            'user', 'nom', 'email', 'tel', 'mdp', 'portfolio', 'annee_experience',
            'disponibilite', 'niveau_d_etude', 'photo', 'adresse',
            'score_performance', 'autres_competences', 'cv', 'competences'
        ]

    def validate(self, data):
        user_data = data.get('user', {})
        user_data['username'] = data.get('nom', user_data.get('username', ''))
        user_data['email'] = data.get('email', user_data.get('email', ''))
        user_data['password'] = data.get('mdp', user_data.get('password', ''))
        data['user'] = user_data
        if not data['user']['username'] or not data['user']['email'] or not data['user']['password']:
            raise serializers.ValidationError("Les champs nom, email et mdp sont requis.")
        if Professionnel.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("Cet email est déjà utilisé.")
        
        # Valider les compétences
        competences = data.get('competences', '')
        competences_list = []
        if competences:
            try:
                competences_list = [int(c.strip()) for c in competences.split(',') if c.strip()]
            except ValueError:
                logger.error(f"Invalid competence IDs: {competences}")
                raise serializers.ValidationError("Tous les IDs de compétences doivent être des entiers.")
            
            for sous_domaine_id in competences_list:
                if not SousDomaine.objects.filter(id=sous_domaine_id).exists():
                    logger.error(f"SousDomaine avec ID {sous_domaine_id} n'existe pas.")
                    raise serializers.ValidationError(f"SousDomaine avec ID {sous_domaine_id} n'existe pas.")
        
        data['competences'] = competences_list
        return data

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        competences = validated_data.pop('competences', [])
        logger.info(f"Creating professionnel with competences: {competences}")
        user = UserSerializer().create(user_data)
        validated_data['mdp'] = make_password(validated_data['mdp'])
        professionnel = Professionnel.objects.create(
            user=user,
            nom=validated_data['nom'],
            email=validated_data['email'],
            tel=validated_data['tel'],
            mdp=validated_data['mdp'],
            portfolio=validated_data.get('portfolio'),
            annee_experience=validated_data['annee_experience'],
            disponibilite=validated_data['disponibilite'],
            niveau_d_etude=validated_data['niveau_d_etude'],
            photo=validated_data['photo'],
            adresse=validated_data['adresse'],
            score_performance=validated_data.get('score_performance', 0.0),
            autres_competences=validated_data.get('autres_competences', 'Aucune'),
            cv=validated_data['cv']
        )
        for sous_domaine_id in competences:
            try:
                Competence.objects.create(
                    sous_domaine_id=sous_domaine_id,
                    professionnel=professionnel
                )
                logger.info(f"Created Competence for sous_domaine_id: {sous_domaine_id}")
            except Exception as e:
                logger.error(f"Failed to create Competence for sous_domaine_id {sous_domaine_id}: {str(e)}")
        send_confirmation_email(professionnel.email, 'professionnel')
        return professionnel