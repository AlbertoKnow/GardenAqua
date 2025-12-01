"""
Context processors para el catálogo.

Hace disponibles las categorías en todas las plantillas.
"""
from .models import Categoria


def categorias(request):
    """
    Añade las categorías activas al contexto de todas las plantillas.
    
    Esto permite que el menú de navegación muestre las categorías
    sin importar desde qué vista se cargue la página.
    
    Retorna:
        dict: Diccionario con las categorías disponibles como 'categorias'.
    """
    return {
        'categorias': Categoria.objects.filter(activo=True).order_by('orden', 'nombre')
    }
