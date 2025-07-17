# profils/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AdministrateurViewSet, ProfessionnelViewSet

router = DefaultRouter()
router.register(r'administrateurs', AdministrateurViewSet)
router.register(r'professionnels', ProfessionnelViewSet)

urlpatterns = [
    path('', include(router.urls)),
]