"""
Configuración base y utilidades para los scripts de productos.
"""
import os
import sys
import django

# Configurar Django
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gardenaqua.settings')
django.setup()

from apps.catalogo.models import Marca, Categoria, Producto, Presentacion
from decimal import Decimal


def obtener_marca(nombre):
    """Obtiene una marca por nombre."""
    try:
        return Marca.objects.get(nombre=nombre)
    except Marca.DoesNotExist:
        print(f"❌ Marca '{nombre}' no encontrada")
        return None


def obtener_categoria(nombre):
    """Obtiene una categoría por nombre."""
    try:
        return Categoria.objects.get(nombre=nombre)
    except Categoria.DoesNotExist:
        print(f"❌ Categoría '{nombre}' no encontrada")
        return None


def crear_producto(nombre, categoria, marca, descripcion, presentaciones, destacado=False):
    """
    Crea un producto con sus presentaciones si no existe.
    
    Args:
        nombre: Nombre del producto
        categoria: Objeto Categoria
        marca: Objeto Marca
        descripcion: HTML con la descripción
        presentaciones: Lista de dicts con 'nombre' y 'precio'
        destacado: Si el producto es destacado
    
    Returns:
        Producto creado o None si ya existe
    """
    if Producto.objects.filter(nombre=nombre).exists():
        print(f"⚠️  '{nombre}' ya existe. Saltando...")
        return None
    
    producto = Producto.objects.create(
        nombre=nombre,
        categoria=categoria,
        marca=marca,
        descripcion=descripcion,
        activo=True,
        destacado=destacado,
    )
    print(f"✅ {nombre}")
    
    for i, pres in enumerate(presentaciones):
        Presentacion.objects.create(
            producto=producto,
            nombre=pres['nombre'],
            precio=Decimal(str(pres['precio'])),
            stock=50,
            orden=i,
        )
    
    return producto
