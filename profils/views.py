from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from authentification.permissions import IsAdministrateur, IsEntreprise, IsProfessionnel
from .models import Administrateur, Entreprise, Professionnel, Categorie, SousDomaine, Newsletters_subscribers, Contact
from .serializers import AdministrateurSerializer, EntrepriseRegistrationSerializer, ProfessionnelSerializer, CategorieSerializer, SousDomaineSerializer, Newsletters_subscribersSerializer, ContactSerializer

class StandardPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class AdministrateurViewSet(viewsets.ModelViewSet):
    queryset = Administrateur.objects.all().order_by('id_administrateur')
    serializer_class = AdministrateurSerializer
    permission_classes = [IsAuthenticated, IsAdministrateur]  # Only admins can access
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['nom', 'email']

    def get_queryset(self):
        # Restrict admins to see only their own profile unless superuser
        user = self.request.user
        if user.is_authenticated and not user.is_superuser:
            return self.queryset.filter(user=user)
        return self.queryset

    def perform_create(self, serializer):
        # Link the created admin to the authenticated user
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save()

class EntrepriseViewSet(viewsets.ModelViewSet):
    queryset = Entreprise.objects.all().order_by('id_entreprise')
    serializer_class = EntrepriseRegistrationSerializer
    permission_classes = [IsAuthenticated, IsEntreprise | IsAdministrateur]  # Only enterprises can access
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['nom', 'email', 'secteur', 'type_abonnement']

    def get_queryset(self):
        # Restrict enterprises to see only their own profile unless admin
        user = self.request.user
        if user.is_authenticated and not user.is_superuser:
            return self.queryset.filter(user=user)
        return self.queryset

    def perform_create(self, serializer):
        # Link the created enterprise to the authenticated user
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save()

class ProfessionnelViewSet(viewsets.ModelViewSet):
    queryset = Professionnel.objects.all().order_by('id_professionnel')
    serializer_class = ProfessionnelSerializer
    permission_classes = [IsAuthenticated, IsProfessionnel | IsAdministrateur]  # Professionals and admins can access
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['nom', 'email', 'annee_experience', 'niveau_d_etude', 'status', 'en_mission']

    def get_queryset(self):
        # Restrict professionals to see only their own profile unless admin
        user = self.request.user
        if user.is_authenticated and not IsAdministrateur().has_permission(self.request, self):
            return self.queryset.filter(user=user)
        return self.queryset

    def perform_create(self, serializer):
        # Link the created professional to the authenticated user
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save()



class CategorieViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer
    permission_classes = [AllowAny]  # Accessible à tous

class SousDomaineViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SousDomaine.objects.all()
    serializer_class = SousDomaineSerializer
    permission_classes = [AllowAny]  # Accessible à tous

    def get_queryset(self):
        queryset = super().get_queryset()
        categorie_id = self.request.query_params.get('categorie')
        if categorie_id:
            queryset = queryset.filter(categorie_id=categorie_id)
        return queryset
    
"""
class NewsLetterViewSet(viewsets.ReadOnlyModelViewSet):#Cette api doit etre retirer avant la mise en production
    queryset = Newsletters_subscribers.objects.all()
    serializer_class = Newsletters_subscribersSerializer
    permission_classes = [AllowAny]#Accessible a tous


class ContactViewSet(viewsets.ReadOnlyModelViewSet):#Pareil que cet api
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [AllowAny]
"""