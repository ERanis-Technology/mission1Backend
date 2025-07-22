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
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Administrateur, CustomUser, Professionnel
from .serializers import AdministrateurSerializer, ProfessionnelSerializer
from .forms import AdminSignupForm, ProfSignupForm, EntrepriseSignupForm

class AdministrateurViewSet(viewsets.ModelViewSet):
    queryset = Administrateur.objects.all()
    serializer_class = AdministrateurSerializer

    @action(detail=False, methods=['post'])
    def validate_professional(self, request):
        professionnel_id = request.data.get('professionnel_id')
        try:
            professionnel = Professionnel.objects.get(id=professionnel_id)
            if professionnel.test_psychologique_passe:
                professionnel.valide_par_admin = True
                professionnel.user.is_active = True
                professionnel.user.save()
                professionnel.save()
                return Response({'status': 'Professionnel validé'})
            return Response({'error': 'Test psychologique non complété'}, status=400)
        except Professionnel.DoesNotExist:
            return Response({'error': 'Professionnel non trouvé'}, status=404)

class ProfessionnelViewSet(viewsets.ModelViewSet):
    queryset = Professionnel.objects.all()
    serializer_class = ProfessionnelSerializer

def signup(request):
    if request.method == 'POST':
        user_type = request.POST.get('user_type')
        if user_type == 'admin':
            form = AdminSignupForm(request.POST)
        elif user_type == 'prof':
            form = ProfSignupForm(request.POST, request.FILES)
        elif user_type == 'ent':
            form = EntrepriseSignupForm(request.POST)
        else:
            return render(request, 'signup.html', {'error': 'Type d’utilisateur invalide'})

        if form.is_valid():
            user = form.save()
            if user_type == 'prof':
                # Store user ID in session for psychological test
                request.session['pending_professional_id'] = user.id
                return redirect('psychological_test')
            else:
                login(request, user, backend='profils.backends.CustomAuthBackend')
                return redirect('home')
        return render(request, 'signup.html', {'form': form, 'user_type': user_type})
    else:
        user_type = request.GET.get('user_type', 'prof')
        if user_type == 'admin':
            form = AdminSignupForm()
        elif user_type == 'prof':
            form = ProfSignupForm()
        elif user_type == 'ent':
            form = EntrepriseSignupForm()
        else:
            form = None
        return render(request, 'signup.html', {'form': form, 'user_type': user_type})

def psychological_test(request):
    professional_id = request.session.get('pending_professional_id')
    if not professional_id:
        return redirect('signup')  # Redirect if no professional ID in session
    try:
        user = CustomUser.objects.get(id=professional_id, user_type='prof')
    except CustomUser.DoesNotExist:
        return redirect('signup')

    if request.method == 'POST':
        professionnel = Professionnel.objects.get(user=user)
        professionnel.test_psychologique_passe = True
        professionnel.save()
        return redirect('waiting_for_validation')
    return render(request, 'psychological_test.html', {'user': user})

def waiting_for_validation(request):
    professional_id = request.session.get('pending_professional_id')
    if not professional_id:
        return redirect('signup')
    try:
        user = CustomUser.objects.get(id=professional_id, user_type='prof')
    except CustomUser.DoesNotExist:
        return redirect('signup')
    return render(request, 'waiting_for_validation.html', {'user': user})
def custom_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user, backend='profils.backends.CustomAuthBackend')
            # Clear session data
            request.session.pop('pending_professional_id', None)
            return redirect('home')
        return render(request, 'login.html', {'error': 'Email, mot de passe incorrect ou compte non validé.'})
    return render(request, 'login.html')

def home(request):
    return render(request, 'home.html')