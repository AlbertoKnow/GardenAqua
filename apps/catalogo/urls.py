"""
Configuración de URLs para la aplicación de catálogo.

Define las rutas para el listado de productos, filtrado por categorías
y detalle de productos.
"""

from django.urls import path

from . import views

app_name = 'catalogo'

urlpatterns = [
    # Página de inicio
    path('', views.inicio, name='inicio'),
    
    # Listado de todos los productos
    path('productos/', views.ProductoListView.as_view(), name='producto_lista'),
    
    # Listado de productos filtrado por categoría
    path(
        'categoria/<slug:categoria_slug>/',
        views.ProductoListView.as_view(),
        name='categoria_detalle'
    ),
    
    # Detalle de un producto
    path(
        'producto/<slug:slug>/',
        views.ProductoDetailView.as_view(),
        name='producto_detalle'
    ),
]
