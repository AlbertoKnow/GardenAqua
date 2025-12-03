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


# URLs de imágenes de productos Seachem Tidal (CDN oficial)
IMAGENES_TIDAL = {
    'filtro-tidal-35-seachem': [
        'https://www.seachem.com/img/products/tidal-35.png',
    ],
    'filtro-tidal-55-seachem': [
        'https://www.seachem.com/img/products/tidal-55.png',
    ],
    'filtro-tidal-75-seachem': [
        'https://www.seachem.com/img/products/tidal-75.png',
    ],
    'filtro-tidal-110-seachem': [
        'https://www.seachem.com/img/products/tidal-110.png',
    ],
}

# URLs de imágenes de plantas acuáticas (Wikimedia Commons - dominio público)
IMAGENES_PLANTAS = {
    'vallisneria-spiralis': [
        'https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Vallisneria_spiralis.jpg/440px-Vallisneria_spiralis.jpg',
    ],
    'echinodorus-bleheri': [
        'https://upload.wikimedia.org/wikipedia/commons/thumb/7/71/Echinodorus_bleheri.jpg/440px-Echinodorus_bleheri.jpg',
    ],
    'cryptocoryne-wendtii-green': [
        'https://upload.wikimedia.org/wikipedia/commons/thumb/d/d2/Cryptocoryne_wendtii.jpg/440px-Cryptocoryne_wendtii.jpg',
    ],
    'anubias-barteri': [
        'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Anubias_barteri_var._nana.jpg/440px-Anubias_barteri_var._nana.jpg',
    ],
    'eleocharis-parvula': [
        'https://upload.wikimedia.org/wikipedia/commons/thumb/7/78/Eleocharis_parvula.jpg/440px-Eleocharis_parvula.jpg',
    ],
    'staurogyne-repens': [
        'https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/Staurogyne_repens.jpg/440px-Staurogyne_repens.jpg',
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
