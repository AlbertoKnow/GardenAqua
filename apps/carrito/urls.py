"""
URLs para la app carrito.
"""
from django.urls import path
from . import views

app_name = 'carrito'

urlpatterns = [
    path('', views.carrito_detalle, name='detalle'),
    path('agregar/<int:presentacion_id>/', views.carrito_agregar, name='agregar'),
    path('eliminar/<int:presentacion_id>/', views.carrito_eliminar, name='eliminar'),
    path('actualizar/<int:presentacion_id>/', views.carrito_actualizar, name='actualizar'),
    path('limpiar/', views.carrito_limpiar, name='limpiar'),
]
