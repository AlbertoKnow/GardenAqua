"""
Context processors para el carrito.

Hace disponible el carrito en todas las plantillas.
"""
from .carrito import Carrito


def carrito(request):
    """
    Añade el carrito al contexto de todas las plantillas.
    
    Retorna:
        dict: Diccionario con el carrito disponible como 'carrito'.
    """
    return {'carrito': Carrito(request)}
