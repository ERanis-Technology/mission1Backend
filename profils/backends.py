from django.contrib.auth.backends import ModelBackend
from .models import CustomUser, Professionnel

class CustomAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = CustomUser.objects.get(email=username)
            if user.check_password(password):
                if user.user_type == 'prof':
                    try:
                        professionnel = Professionnel.objects.get(user=user)
                        if not professionnel.test_psychologique_passe or not professionnel.valide_par_admin:
                            return None
                    except Professionnel.DoesNotExist:
                        return None
                return user
            return None
        except CustomUser.DoesNotExist:
            return None