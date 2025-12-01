"""
URLs para la app pedidos.
"""
from django.urls import path
from . import views

app_name = 'pedidos'

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('confirmacion/<str:numero_pedido>/', views.confirmacion, name='confirmacion'),
    path('consultar/', views.consultar_pedido, name='consultar'),
]
