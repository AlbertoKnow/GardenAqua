"""
Configuración de URLs para el proyecto GardenAqua.

Este archivo define las rutas principales del proyecto, incluyendo
el panel de administración y las aplicaciones del ecommerce.

Para más información, ver:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Panel de administración
    path('admin/', admin.site.urls),
    
    # Aplicaciones del proyecto
    path('', include('apps.catalogo.urls', namespace='catalogo')),
    path('carrito/', include('apps.carrito.urls', namespace='carrito')),
    path('pedido/', include('apps.pedidos.urls', namespace='pedidos')),
]

# Servir archivos multimedia en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
