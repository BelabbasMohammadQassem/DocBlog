from django.urls import path
from django.contrib.auth import views as auth_view
from . import views
from .views import custom_logout
from .views import register

urlpatterns = [
    path('', views.index, name='index'),
    path('article/<int:article_id>/', views.article_detail, name='article_detail'),
    path('about/', views.about, name='about'),
    path('search/', views.search_articles, name='search_articles'),
    path('category/<int:category_id>/', views.articles_by_category, name='articles_by_category'),
    path('login/', auth_view.LoginView.as_view(template_name='polls/login.html'), name='login'),
    path("logout/", custom_logout, name="logout"),
    path("register/", register, name="register"),
    path('comment/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    ]