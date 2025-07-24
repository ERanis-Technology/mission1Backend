# profils/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AdministrateurViewSet, EntrepriseViewSet, ProfessionnelViewSet, CategorieViewSet, SousDomaineViewSet

router = DefaultRouter()
router.register(r'administrateurs', AdministrateurViewSet)
router.register(r'entreprises', EntrepriseViewSet)
router.register(r'professionnels', ProfessionnelViewSet)
router.register(r'categories', CategorieViewSet)
router.register(r'sous-domaines', SousDomaineViewSet)

urlpatterns = [
    path('', include(router.urls)),
]