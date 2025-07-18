from django.http import HttpResponse
from .models import Article, Category, Comment
from .forms import CommentForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import logout
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required



def index(request):
    """
    Affiche la page d'accueil avec la liste des articles triés par date de publication (du plus récent au plus ancien).

    Args:
        request (HttpRequest): La requête HTTP envoyée par l'utilisateur.

    Returns:
        HttpResponse: La page HTML contenant la liste des articles.
    """
    articles = Article.objects.all().order_by('-pub_date')
    return render (request, 'polls/index.html', {'articles' : articles})
    
def article_detail(request, article_id):
    """
    Affiche le détail d'un article ainsi que ses commentaires, et permet aux utilisateurs authentifiés du groupe 'user' d'en poster un.

    Args:
        request (HttpRequest): La requête HTTP envoyée par l'utilisateur.
        article_id (int): L'identifiant de l'article à afficher.

    Returns:
        HttpResponse: La page HTML avec les détails de l'article, les commentaires existants, 
        et un formulaire pour en ajouter un (si l'utilisateur a les droits).
    """
    article = get_object_or_404(Article, pk=article_id)
    comments = article.comments.order_by('-created_at')

    if request.method == 'POST':
        if request.user.is_authenticated:
            if request.user.groups.filter(name='user').exists():
                form = CommentForm(request.POST)
                if form.is_valid():
                    comment = form.save(commit=False)
                    comment.article = article
                    comment.user = request.user
                    comment.save()
                    return redirect('article_detail', article_id=article.pk)
            else:
                messages.warning(request, "Tu dois avoir le rôle 'user' pour commenter.")
                return redirect('article_detail', article_id=article.pk)
        else:
            return redirect('login')
    else:
        form = CommentForm()

    return render(request, 'polls/article_detail.html', {
        'article': article,
        'comments': comments,
        'form': form,
    })

def edit_comment(request, comment_id):
    """
    Permet à un utilisateur authentifié (du groupe 'user') de modifier un commentaire qu’il a écrit.

    Args:
        request (HttpRequest): La requête HTTP en cours.
        comment_id (int): L'identifiant du commentaire à modifier.

    Returns:
        HttpResponse: 
            - Redirige vers la page de l'article si l'utilisateur n'a pas les droits.
            - Si POST valide, enregistre le commentaire modifié et redirige vers l'article.
            - Sinon, affiche le formulaire pré-rempli pour modification.
    """
    comment = get_object_or_404(Comment, pk=comment_id)

    if not request.user.groups.filter(name='user').exists() or request.user !=comment.user:
        messages.error(request, "Tu n'es pas autorisé à modifier ce commentaire.")
        return redirect('article_detail', article_id=comment.article.id)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, "Commentaire mis à jour.")
            return redirect('article_detail', article_id=comment.article.id)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'polls/edit_comment.html', {
        'form': form,
        'comment': comment
    })

@login_required
def delete_comment(request, comment_id):
    """
    Supprime un commentaire si l'utilisateur est l'auteur et appartient au groupe 'user'.

    Args:
        request (HttpRequest): La requête HTTP envoyée par l'utilisateur.
        comment_id (int): L'identifiant du commentaire à supprimer.

    Returns:
        HttpResponseRedirect: 
            - Redirige vers la page de l'article après suppression.
            - Redirige avec un message d'erreur si l'utilisateur n'est pas autorisé.
    """
    comment = get_object_or_404(Comment, pk=comment_id)

    if not request.user.groups.filter(name='user').exists() or request.user != comment.user:
        messages.error(request, "Tu n'es pas autorisé à supprimer ce commentaire.")
        return redirect('article_detail', article_id=comment.article.id)

    if request.method == 'POST':
        comment.delete()
        messages.success(request, "Commentaire supprimé.")
    return redirect('article_detail', article_id=comment.article.id)


def about(request):
    """
    Affiche la page 'À propos'.

    Args:
        request (HttpRequest): La requête HTTP entrante.

    Returns:
        HttpResponse: La réponse contenant le template 'polls/about.html'.
    """
    return render(request, 'polls/about.html')

def search_articles(request):
    """
    Permet la recherche d'articles à partir d'une requête dans l'URL (paramètre 'q').

    - Si la requête contient au moins 3 caractères :
        - Redirige vers l'article si un seul résultat est trouvé.
        - Sinon, affiche la liste des résultats.
    - Sinon, affiche un message d'erreur.

    Args:
        request (HttpRequest): La requête HTTP contenant éventuellement le paramètre 'q'.

    Returns:
        HttpResponse: 
            - Redirection vers un article unique trouvé.
            - Template 'search_results.html' avec résultats ou message d'erreur.
    """
    query = request.GET.get('q')
    if query and len(query) >= 3:
        results = Article.objects.filter(title__icontains=query)
        if results.count() == 1:
            return redirect('article_detail', article_id=results.first().id)
        else:
            return render(request, 'polls/search_results.html', {'results': results, 'query': query})
    else:
        
        return render(request, 'polls/search_results.html', {
            'results': [],
            'query': query,
            'error': "Veuillez entrer au moins 3 caractères pour effectuer une recherche."
        })

def articles_by_category(request, category_id):
    """
    Affiche les articles appartenant à une catégorie spécifique.

    Args:
        request (HttpRequest): La requête HTTP.
        category_id (int): L'ID de la catégorie à afficher.

    Returns:
        HttpResponse: Le rendu du template avec les articles filtrés par catégorie.
    """
    category = get_object_or_404(Category, pk=category_id)
    articles = Article.objects.filter(categorie=category).order_by('-pub_date')
    return render(request, 'polls/articles_by_category.html', {
        'category': category,
        'articles': articles
    }
    )

def custom_logout(request):
    """
     Déconnecte l'utilisateur et le redirige vers la page d'accueil.

    Args:
        request (HttpRequest): La requête HTTP.

    Returns:
        HttpResponseRedirect: Redirection vers la page d'accueil ('index').
    """
    logout(request)
    return redirect('index')

def register(request):
    """
    Gère l'inscription d'un nouvel utilisateur.

    - Affiche le formulaire d'inscription.
    - Valide et enregistre l'utilisateur si la requête est POST et valide.
    - Assigne l'utilisateur au groupe "user" par défaut.

    Args:
        request (HttpRequest): La requête HTTP.

    Returns:
        HttpResponse: Le template d'inscription ou une redirection vers la page de connexion.
    """
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            group, created = Group.objects.get_or_create(name='user')
            user.groups.add(group)
            user.save()

            messages.success(request, "Inscription réussie ! Tu peux maintenant te connecter.")
            return redirect('login')
        else:
            print(form.errors) 
    else:
        form = RegisterForm()
    return render(request, 'polls/register.html', {'form': form})


