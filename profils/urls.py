# profils/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AdministrateurViewSet, EntrepriseViewSet, ProfessionnelViewSet, CategorieViewSet, SousDomaineViewSet, NewsLetterViewSet,ContactViewSet

router = DefaultRouter()
router.register(r'administrateurs', AdministrateurViewSet)
router.register(r'entreprises', EntrepriseViewSet)
router.register(r'professionnels', ProfessionnelViewSet)
router.register(r'categories', CategorieViewSet)
router.register(r'sous-domaines', SousDomaineViewSet)
router.register(r'newsletter',NewsLetterViewSet)
router.register(r"contact",ContactViewSet)

urlpatterns = [
    path('', include(router.urls)),
]