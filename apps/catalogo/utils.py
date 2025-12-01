"""
Utilidades para el procesamiento de imágenes.

Este módulo contiene funciones para optimizar imágenes subidas,
incluyendo conversión a WebP y redimensionamiento.
"""

import os
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile


# Configuración de tamaños de imagen
IMAGE_SIZES = {
    'thumbnail': (150, 150),   # Para listados pequeños
    'card': (400, 400),         # Para tarjetas de productos
    'detail': (800, 800),       # Para vista de detalle
    'full': (1200, 1200),       # Tamaño máximo
}

# Calidad de compresión WebP (0-100)
WEBP_QUALITY = 85


def procesar_imagen(imagen_field, max_size=IMAGE_SIZES['full'], quality=WEBP_QUALITY):
    """
    Procesa una imagen: la convierte a WebP y la redimensiona.
    
    Esta función toma un campo de imagen de Django, lo convierte
    al formato WebP optimizado y lo redimensiona si excede el
    tamaño máximo especificado.
    
    Args:
        imagen_field: Campo ImageField de Django con la imagen a procesar.
        max_size (tuple): Tupla (ancho, alto) con el tamaño máximo.
        quality (int): Calidad de compresión WebP (0-100).
    
    Returns:
        ContentFile: Nuevo archivo de imagen en formato WebP.
        str: Nuevo nombre del archivo con extensión .webp.
    
    Ejemplo:
        >>> nuevo_contenido, nuevo_nombre = procesar_imagen(self.imagen)
        >>> self.imagen.save(nuevo_nombre, nuevo_contenido, save=False)
    """
    # Abrir la imagen con Pillow
    img = Image.open(imagen_field)
    
    # Convertir a RGB si es necesario (para PNG con transparencia)
    if img.mode in ('RGBA', 'LA', 'P'):
        # Crear fondo blanco para imágenes con transparencia
        background = Image.new('RGB', img.size, (255, 255, 255))
        if img.mode == 'P':
            img = img.convert('RGBA')
        background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
        img = background
    elif img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Redimensionar si excede el tamaño máximo (mantiene proporción)
    img.thumbnail(max_size, Image.Resampling.LANCZOS)
    
    # Guardar en formato WebP
    buffer = BytesIO()
    img.save(buffer, format='WEBP', quality=quality, optimize=True)
    buffer.seek(0)
    
    # Generar nuevo nombre con extensión .webp
    nombre_original = os.path.splitext(imagen_field.name)[0]
    # Extraer solo el nombre del archivo, sin la ruta
    nombre_base = os.path.basename(nombre_original)
    nuevo_nombre = f"{nombre_base}.webp"
    
    return ContentFile(buffer.read()), nuevo_nombre


def necesita_conversion(imagen_field):
    """
    Verifica si una imagen necesita ser convertida a WebP.
    
    Args:
        imagen_field: Campo ImageField de Django.
    
    Returns:
        bool: True si la imagen no es WebP, False si ya lo es.
    """
    if not imagen_field:
        return False
    
    nombre = imagen_field.name.lower()
    return not nombre.endswith('.webp')


def obtener_dimensiones(imagen_field):
    """
    Obtiene las dimensiones de una imagen.
    
    Args:
        imagen_field: Campo ImageField de Django.
    
    Returns:
        tuple: (ancho, alto) de la imagen.
    """
    with Image.open(imagen_field) as img:
        return img.size


def imagen_excede_tamaño(imagen_field, max_size=IMAGE_SIZES['full']):
    """
    Verifica si una imagen excede el tamaño máximo permitido.
    
    Args:
        imagen_field: Campo ImageField de Django.
        max_size (tuple): Tupla (ancho, alto) con el tamaño máximo.
    
    Returns:
        bool: True si la imagen excede el tamaño, False en caso contrario.
    """
    ancho, alto = obtener_dimensiones(imagen_field)
    return ancho > max_size[0] or alto > max_size[1]
