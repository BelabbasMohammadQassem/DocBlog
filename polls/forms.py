from django import forms
from .models import Comment
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CommentForm(forms.ModelForm):
    """
    Formulaire pour créer ou modifier un commentaire.

    Champs :
        content (Textarea) : champ texte pour le contenu du commentaire,
                             affiché avec 3 lignes et un placeholder.

    Utilisation :
        Utilisé pour valider et traiter les données de commentaire soumises par l'utilisateur.
    """
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows':3, 'placeholder': 'Ton commentaire...'})
        }

class RegisterForm(UserCreationForm):
    """
    Formulaire d'inscription personnalisé utilisant l'adresse email comme identifiant.

    Champs :
        email (EmailField) : champ obligatoire pour l'adresse email de l'utilisateur.
        password1, password2 : champs pour la saisie et la confirmation du mot de passe.

    Méthodes personnalisées :
        clean_email() : vérifie que l'adresse email n'est pas déjà utilisée dans la base.

    Utilisation :
        Permet d'inscrire un nouvel utilisateur avec email et mot de passe.
    """
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Cette adresse email est déjà utilisée.")
        return email
