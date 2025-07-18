# profils/views.py
"""
from rest_framework import viewsets, permissions
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import Administrateur, Professionnel
from .serializers import AdministrateurSerializer, ProfessionnelSerializer

class StandardPagination(PageNumberPagination):
    page_size = 10  # Limite à 10 objets par page
    page_size_query_param = 'page_size'
    max_page_size = 100

class AdministrateurViewSet(viewsets.ModelViewSet):
    queryset = Administrateur.objects.all().order_by('id_administrateur')
    serializer_class = AdministrateurSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]  # Accès réservé aux admins
    pagination_class = StandardPagination  # Active la pagination
    filter_backends = [DjangoFilterBackend]  # Permet le filtrage
    filterset_fields = ['nom', 'email']  # Champs filtrables

    def perform_create(self, serializer):
        # Validation supplémentaire lors de la création
        serializer.save()

    def perform_update(self, serializer):
        # Validation supplémentaire lors de la mise à jour
        serializer.save()

class ProfessionnelViewSet(viewsets.ModelViewSet):
    queryset = Professionnel.objects.all().order_by('id_professionnel')
    serializer_class = ProfessionnelSerializer
    permission_classes = [permissions.IsAuthenticated]  # Accès réservé aux utilisateurs authentifiés
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['nom', 'email']

    def get_queryset(self):
        # Optimisation : filtrer dynamiquement selon l'utilisateur connecté (exemple)
        user = self.request.user
        if user.is_authenticated and not user.is_staff:
            return self.queryset.filter(email=user.email)
        return self.queryset

    def perform_create(self, serializer):
        # Validation ou logique supplémentaire
        serializer.save()

    def perform_update(self, serializer):
        # Validation ou logique supplémentaire
        serializer.save()
        """

# profils/views.py
from rest_framework import viewsets
from .models import Administrateur, Professionnel
from .serializers import AdministrateurSerializer, ProfessionnelSerializer

class AdministrateurViewSet(viewsets.ModelViewSet):
    queryset = Administrateur.objects.all()
    serializer_class = AdministrateurSerializer

class ProfessionnelViewSet(viewsets.ModelViewSet):
    queryset = Professionnel.objects.all()
    serializer_class = ProfessionnelSerializer
    
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignupForm

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            if user.user_type == 'prof':
                Professionnel.objects.create(user=user, nom=request.POST.get('nom'))
            elif user.user_type == 'ent':
                Entreprise.objects.create(user=user, nom=request.POST.get('nom'))
            elif user.user_type == 'admin':
                Administrateur.objects.create(user=user, nom=request.POST.get('nom'))
            login(request, user)
            return redirect('home')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})