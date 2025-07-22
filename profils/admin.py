from django.contrib import admin
"""
from .models import Abonnement, Type, Administrateur, Professionnel, SouscriptionProf, Competence

@admin.register(Abonnement)
class AbonnementAdmin(admin.ModelAdmin):
    list_display = ('id_admin', 'nom', 'email', 'annee_arrivee', 'statut', 'photo')
    search_fields = ('nom', 'email')
    list_filter = ('statut', 'annee_arrivee')

@admin.register(Type)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('id_admin', 'nom', 'email', 'annee_arrivee', 'statut', 'photo')
    search_fields = ('nom', 'email')
    list_filter = ('statut', 'annee_arrivee')

@admin.register(Administrateur)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('id_admin', 'nom', 'email', 'annee_arrivee', 'statut', 'photo')
    search_fields = ('nom', 'email')
    list_filter = ('statut', 'annee_arrivee')

@admin.register(Professionnel)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('id_admin', 'nom', 'email', 'annee_arrivee', 'statut', 'photo')
    search_fields = ('nom', 'email')
    list_filter = ('statut', 'annee_arrivee')

@admin.register(SouscriptionProf)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('id_admin', 'nom', 'email', 'annee_arrivee', 'statut', 'photo')
    search_fields = ('nom', 'email')
    list_filter = ('statut', 'annee_arrivee')

@admin.register(Competence)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('id_admin', 'nom', 'email', 'annee_arrivee', 'statut', 'photo')
    search_fields = ('nom', 'email')
    list_filter = ('statut', 'annee_arrivee')"""

from .models import CustomUser, Administrateur, Professionnel, Entreprise, Type, Abonnement, SouscriptionProf, Competence

@admin.register(Professionnel)
class ProfessionnelAdmin(admin.ModelAdmin):
    list_display = ['nom', 'prenom', 'email', 'test_psychologique_passe', 'valide_par_admin']
    list_filter = ['valide_par_admin', 'test_psychologique_passe']
    actions = ['validate_professionals']

    def email(self, obj):
        return obj.user.email

    def validate_professionals(self, request, queryset):
        queryset.update(valide_par_admin=True)
        for prof in queryset:
            prof.user.is_active = True
            prof.user.save()
    validate_professionals.short_description = "Valider les professionnels sélectionnés"

admin.site.register(CustomUser)
admin.site.register(Administrateur)
admin.site.register(Entreprise)
admin.site.register(Type)
admin.site.register(Abonnement)
admin.site.register(SouscriptionProf)
admin.site.register(Competence)