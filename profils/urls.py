from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AdministrateurViewSet, ProfessionnelViewSet, signup, psychological_test, waiting_for_validation, custom_login, home

router = DefaultRouter()
router.register(r'administrateurs', AdministrateurViewSet)
router.register(r'professionnels', ProfessionnelViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('signup/', signup, name='signup'),
    path('psychological-test/', psychological_test, name='psychological_test'),
    path('waiting-for-validation/', waiting_for_validation, name='waiting_for_validation'),
    path('login/', custom_login, name='login'),
    path('home/', home, name='home'),  # Changed to avoid conflict with router.urls
]