from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from profils.models import Administrateur, Entreprise, Professionnel
from .serializers import (AdministrateurRegistrationSerializer, EntrepriseRegistrationSerializer,
                          ProfessionnelRegistrationSerializer, LoginSerializer)
import logging
from rest_framework.permissions import AllowAny

logger = logging.getLogger(__name__)

class AdministrateurRegistrationView(APIView):
    def post(self, request):
        serializer = AdministrateurRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Administrateur créé avec succès"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EntrepriseRegistrationView(APIView):
    def post(self, request):
        serializer = EntrepriseRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Entreprise créée avec succès"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProfessionnelRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
    
        serializer = ProfessionnelRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Professionnel créé avec succès"}, status=status.HTTP_201_CREATED)
        logger.error(f"Serializer errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            
            try:
                user = User.objects.get(email=email)
                user = authenticate(username=user.username, password=password)
                if user:
                    refresh = RefreshToken.for_user(user)
                    user_type = None
                    user_data = {}

                    # Check user type and fetch profile data
                    if Administrateur.objects.filter(user=user).exists():
                        user_type = 'administrateur'
                        administrateur = Administrateur.objects.get(user=user)
                        user_data = {
                            'id': administrateur.id_administrateur,
                            'nom': administrateur.nom,
                            'email': administrateur.email,
                        }
                    elif Entreprise.objects.filter(user=user).exists():
                        user_type = 'entreprise'
                        entreprise = Entreprise.objects.get(user=user)
                        user_data = {
                            'id': entreprise.id_entreprise,
                            'nom': entreprise.nom,
                            'email': entreprise.email,
                            'secteur': entreprise.secteur,
                            'type_abonnement': entreprise.type_abonnement,
                        }
                    elif Professionnel.objects.filter(user=user).exists():
                        user_type = 'professionnel'
                        professionnel = Professionnel.objects.get(user=user)
                        user_data = {
                            'id': professionnel.id_professionnel,
                            'nom': professionnel.nom,
                            'email': professionnel.email,
                            'annee_experience': professionnel.annee_experience,
                            'disponibilite': professionnel.disponibilite,
                            'score_performance': professionnel.score_performance,
                        }
                    else:
                        return Response({"error": "Utilisateur non associé à un type valide"}, status=status.HTTP_400_BAD_REQUEST)

                    return Response({
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                        'user_type': user_type,
                        'user_data': user_data,
                    }, status=status.HTTP_200_OK)
                return Response({"error": "Identifiants incorrects"}, status=status.HTTP_401_UNAUTHORIZED)
            except User.DoesNotExist:
                return Response({"error": "Utilisateur non trouvé"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)