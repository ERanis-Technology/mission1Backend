from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (AdministrateurRegistrationView, EntrepriseRegistrationView,
                    ProfessionnelRegistrationView, LoginView)

urlpatterns = [
    path('register/administrateur/', AdministrateurRegistrationView.as_view(), name='administrateur-register'),
    path('register/entreprise/', EntrepriseRegistrationView.as_view(), name='entreprise-register'),
    path('register/professionnel/', ProfessionnelRegistrationView.as_view(), name='professionnel-register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]