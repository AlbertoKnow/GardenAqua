"""
Script para agregar imágenes a los productos existentes.

Descarga imágenes desde URLs públicas y las asocia a los productos
correspondientes en la base de datos.
"""
import os
import sys
import django
import requests
from io import BytesIO
from urllib.parse import urlparse

# Configurar Django
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gardenaqua.settings')
django.setup()

from django.core.files.base import ContentFile
from apps.catalogo.models import Producto, ImagenProducto


# URLs de imágenes de productos Seachem Tidal
IMAGENES_TIDAL = {
    'seachem-tidal-35': [
        'https://seachem.com/img/products/tidal-35.png',
    ],
    'seachem-tidal-55': [
        'https://seachem.com/img/products/tidal-55.png',
    ],
    'seachem-tidal-75': [
        'https://seachem.com/img/products/tidal-75.png',
    ],
    'seachem-tidal-110': [
        'https://seachem.com/img/products/tidal-110.png',
    ],
}

# URLs de imágenes de plantas Tropica (usando sus CDN públicos)
IMAGENES_PLANTAS = {
    'taxiphyllum-barbieri-java-moss': [
        'https://tropica.com/imagegen.ashx?image=/Plants/003%20TC/003%20ATC%20Taxiphyllum%20barbieri%201.jpg&width=600',
    ],
    'microsorum-pteropus-java-fern': [
        'https://tropica.com/imagegen.ashx?image=/Plants/008%20Pot/008%20Pot%20Microsorum%20pteropus%201.jpg&width=600',
    ],
    'anubias-barteri-var-nana': [
        'https://tropica.com/imagegen.ashx?image=/Plants/101%20Pot/101%20Pot%20Anubias%20barteri%20var%20nana%201.jpg&width=600',
    ],
    'bucephalandra-green-wavy': [
        'https://tropica.com/imagegen.ashx?image=/Plants/138%20TC/138%20TC%20Bucephalandra%20Green%20Wavy.jpg&width=600',
    ],
    'echinodorus-bleheri-amazon-sword': [
        'https://tropica.com/imagegen.ashx?image=/Plants/071%20Pot/071%20Pot%20Echinodorus%20bleheri%201.jpg&width=600',
    ],
    'vallisneria-spiralis': [
        'https://tropica.com/imagegen.ashx?image=/Plants/133%20Bunch/133%20Bunch%20Vallisneria%20spiralis%20Leopard%201.jpg&width=600',
    ],
    'eleocharis-acicularis-mini': [
        'https://tropica.com/imagegen.ashx?image=/Plants/132%20TC/132B%20TC%20Eleocharis%20acicularis%20Mini%201.jpg&width=600',
    ],
    'hemianthus-callitrichoides-cuba': [
        'https://tropica.com/imagegen.ashx?image=/Plants/048B%20TC/048B%20TC%20Hemianthus%20callitrichoides%20Cuba%201.jpg&width=600',
    ],
}


def descargar_imagen(url):
    """
    Descarga una imagen desde una URL.
    
    Args:
        url: URL de la imagen a descargar.
        
    Returns:
        tuple: (contenido_bytes, nombre_archivo) o (None, None) si falla.
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        # Obtener nombre del archivo de la URL
        parsed = urlparse(url)
        path = parsed.path
        
        # Determinar extensión
        if '.png' in path.lower():
            extension = 'png'
        elif '.jpg' in path.lower() or '.jpeg' in path.lower():
            extension = 'jpg'
        else:
            # Intentar determinar por content-type
            content_type = response.headers.get('content-type', '')
            if 'png' in content_type:
                extension = 'png'
            else:
                extension = 'jpg'
        
        return response.content, extension
        
    except Exception as e:
        print(f"  ❌ Error descargando {url}: {e}")
        return None, None


def agregar_imagen_producto(producto, url, es_principal=True, orden=0):
    """
    Descarga una imagen y la asocia a un producto.
    
    Args:
        producto: Instancia del modelo Producto.
        url: URL de la imagen a descargar.
        es_principal: Si es la imagen principal del producto.
        orden: Orden de la imagen en la galería.
        
    Returns:
        bool: True si se agregó correctamente, False si falló.
    """
    contenido, extension = descargar_imagen(url)
    
    if contenido is None:
        return False
    
    # Crear nombre de archivo
    nombre_archivo = f"{producto.slug}_{orden}.{extension}"
    
    # Crear la imagen del producto
    imagen = ImagenProducto(
        producto=producto,
        es_principal=es_principal,
        mostrar_en_galeria=True,
        orden=orden,
        alt_text=f"{producto.nombre}"
    )
    
    # Guardar la imagen
    imagen.imagen.save(nombre_archivo, ContentFile(contenido), save=True)
    
    return True


def main():
    """
    Función principal que procesa todos los productos.
    """
    print("=" * 60)
    print("AGREGANDO IMÁGENES A PRODUCTOS")
    print("=" * 60)
    
    todas_imagenes = {**IMAGENES_TIDAL, **IMAGENES_PLANTAS}
    
    for slug, urls in todas_imagenes.items():
        try:
            producto = Producto.objects.get(slug=slug)
            print(f"\n📦 Procesando: {producto.nombre}")
            
            # Verificar si ya tiene imágenes
            imagenes_existentes = producto.imagenes.count()
            if imagenes_existentes > 0:
                print(f"  ⚠️ Ya tiene {imagenes_existentes} imagen(es), saltando...")
                continue
            
            # Agregar cada imagen
            for i, url in enumerate(urls):
                es_principal = (i == 0)
                print(f"  📥 Descargando imagen {i + 1}...")
                
                if agregar_imagen_producto(producto, url, es_principal, i):
                    print(f"  ✅ Imagen agregada correctamente")
                else:
                    print(f"  ❌ No se pudo agregar la imagen")
                    
        except Producto.DoesNotExist:
            print(f"\n⚠️ Producto no encontrado: {slug}")
        except Exception as e:
            print(f"\n❌ Error procesando {slug}: {e}")
    
    print("\n" + "=" * 60)
    print("PROCESO COMPLETADO")
    print("=" * 60)


if __name__ == '__main__':
    main()
