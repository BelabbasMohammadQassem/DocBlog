from .models import Category

def categories(request):
    """
     Récupère toutes les catégories triées par identifiant.

    Args:
        request (HttpRequest): La requête HTTP reçue.

    Returns:
        dict: Un dictionnaire contenant la liste des catégories sous la clé 'categories'.

    Utilisation:
        Cette fonction peut être utilisée comme context processor ou dans une vue pour
        fournir la liste des catégories à un template.
    """
    categories = Category.objects.all().order_by('id')
    return {'categories': categories}