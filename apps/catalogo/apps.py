"""
Configuración de la aplicación Catálogo.

Esta aplicación maneja el catálogo de productos del ecommerce GardenAqua,
incluyendo categorías, productos y sus atributos.
"""

from django.apps import AppConfig


class CatalogoConfig(AppConfig):
    """
    Configuración de la aplicación de catálogo de productos.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.catalogo'
    verbose_name = 'Catálogo de Productos'
