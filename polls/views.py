from django.http import HttpResponse
from .models import Article, Category, Comment
from .forms import CommentForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import logout
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth.models import Group



def index(request):
    articles = Article.objects.all().order_by('-pub_date')
    return render (request, 'polls/index.html', {'articles' : articles})
    
def article_detail(request, article_id):
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



def about(request):
    return render(request, 'polls/about.html')

def search_articles(request):
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
    category = get_object_or_404(Category, pk=category_id)
    articles = Article.objects.filter(categorie=category).order_by('-pub_date')
    return render(request, 'polls/articles_by_category.html', {
        'category': category,
        'articles': articles
    }
    )

def custom_logout(request):
    logout(request)
    return redirect('index')

def register(request):
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


