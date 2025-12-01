"""
Configuración de la app pedidos.
"""
from django.apps import AppConfig


class PedidosConfig(AppConfig):
    """Configuración de la aplicación Pedidos."""
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.pedidos'
    verbose_name = 'Pedidos'
