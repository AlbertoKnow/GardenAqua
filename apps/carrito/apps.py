"""
Configuración de la app carrito.
"""
from django.apps import AppConfig


class CarritoConfig(AppConfig):
    """Configuración de la aplicación Carrito."""
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.carrito'
    verbose_name = 'Carrito de Compras'
