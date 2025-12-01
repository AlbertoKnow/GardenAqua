"""
Modelos para el carrito de compras.

El carrito utiliza sesiones para permitir compras sin registro.
"""
from django.db import models


# El carrito se maneja mediante sesiones, no requiere modelo de base de datos.
# La lógica del carrito está en carrito.py (clase Carrito).
