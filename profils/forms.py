from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Professionnel, Entreprise, Administrateur, Competence

class BaseSignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = CustomUser
        fields = ['email', 'user_type', 'password1', 'password2']

class AdminSignupForm(BaseSignupForm):
    nom = forms.CharField(max_length=100)
    
    class Meta(BaseSignupForm.Meta):
        pass
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'admin'
        if commit:
            user.save()
            Administrateur.objects.create(user=user, nom=self.cleaned_data['nom'])
        return user

class ProfSignupForm(BaseSignupForm):
    nom = forms.CharField(max_length=100)
    prenom = forms.CharField(max_length=100)
    telephone = forms.CharField(max_length=20)
    annee_experience = forms.IntegerField()
    portfolio_link = forms.URLField(required=False)
    cv = forms.FileField()
    domaine_expertise = forms.CharField(max_length=100)
    disponibilites = forms.CharField(max_length=200)
    niveau_etudes = forms.CharField(max_length=100)
    reseau_sociaux = forms.CharField(widget=forms.Textarea, required=False)
    pays = forms.CharField(max_length=100)
    ville = forms.CharField(max_length=100)
    competences = forms.CharField(widget=forms.Textarea, required=True, help_text="Listez vos compétences clés, séparées par des virgules.")

    class Meta(BaseSignupForm.Meta):
        pass
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'prof'
        user.is_active = False  # Inactive until admin validation
        
        if commit:
            user.save()
            prof = Professionnel.objects.create(
                user=user,
                nom=self.cleaned_data['nom'],
                prenom=self.cleaned_data['prenom'],
                telephone=self.cleaned_data['telephone'],
                annee_experience=self.cleaned_data['annee_experience'],
                portfolio_link=self.cleaned_data.get('portfolio_link', ''),
                cv=self.cleaned_data['cv'],
                domaine_expertise=self.cleaned_data['domaine_expertise'],
                disponibilites=self.cleaned_data['disponibilites'],
                niveau_etudes=self.cleaned_data['niveau_etudes'],
                reseau_sociaux=self.cleaned_data.get('reseau_sociaux', ''),
                pays=self.cleaned_data['pays'],
                ville=self.cleaned_data['ville'],
                test_psychologique_passe=False,
                valide_par_admin=False
            )
            # Save competences
            if self.cleaned_data.get('competences'):
                for competence in self.cleaned_data['competences'].split(','):
                    Competence.objects.create(professionnel=prof, nom=competence.strip())
        return user

class EntrepriseSignupForm(BaseSignupForm):
    nom = forms.CharField(max_length=100)
    secteur = forms.CharField(max_length=100)
    besoin = forms.CharField(widget=forms.Textarea)
    
    class Meta(BaseSignupForm.Meta):
        pass
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'ent'
        if commit:
            user.save()
            Entreprise.objects.create(
                user=user,
                nom=self.cleaned_data['nom'],
                secteur=self.cleaned_data['secteur'],
                besoin=self.cleaned_data['besoin']
            )
        return user