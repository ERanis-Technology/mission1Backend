from rest_framework.permissions import BasePermission
from profils.models import Professionnel, Entreprise, Administrateur

class IsProfessionnel(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and Professionnel.objects.filter(user=request.user).exists()

class IsEntreprise(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and Entreprise.objects.filter(user=request.user).exists()

class IsAdministrateur(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and Administrateur.objects.filter(user=request.user).exists()