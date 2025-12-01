"""
Comando de Django para convertir todas las imágenes existentes a WebP.

Este comando recorre todas las imágenes del catálogo (categorías, marcas
e imágenes de productos) y las convierte al formato WebP optimizado.

Uso:
    python manage.py convertir_imagenes_webp
    python manage.py convertir_imagenes_webp --dry-run  # Solo muestra qué se convertiría
"""

import os
from django.core.management.base import BaseCommand
from django.conf import settings

from apps.catalogo.models import Categoria, Marca, ImagenProducto
from apps.catalogo.utils import procesar_imagen, necesita_conversion


class Command(BaseCommand):
    """Comando para convertir imágenes existentes a formato WebP."""
    
    help = 'Convierte todas las imágenes del catálogo a formato WebP optimizado'
    
    def add_arguments(self, parser):
        """Define los argumentos del comando."""
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Muestra qué imágenes se convertirían sin realizar cambios',
        )
    
    def handle(self, *args, **options):
        """Ejecuta la conversión de imágenes."""
        dry_run = options['dry_run']
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING('Modo DRY-RUN: No se realizarán cambios\n')
            )
        
        total_convertidas = 0
        total_errores = 0
        
        # Procesar imágenes de categorías
        self.stdout.write('\n📁 Procesando imágenes de CATEGORÍAS...')
        convertidas, errores = self._procesar_modelo(
            Categoria, 'imagen', dry_run
        )
        total_convertidas += convertidas
        total_errores += errores
        
        # Procesar logos de marcas
        self.stdout.write('\n📁 Procesando logos de MARCAS...')
        convertidas, errores = self._procesar_modelo(
            Marca, 'logo', dry_run
        )
        total_convertidas += convertidas
        total_errores += errores
        
        # Procesar imágenes de productos
        self.stdout.write('\n📁 Procesando imágenes de PRODUCTOS...')
        convertidas, errores = self._procesar_modelo(
            ImagenProducto, 'imagen', dry_run
        )
        total_convertidas += convertidas
        total_errores += errores
        
        # Resumen final
        self.stdout.write('\n' + '=' * 50)
        if dry_run:
            self.stdout.write(
                self.style.WARNING(f'Se convertirían {total_convertidas} imágenes')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f'✅ {total_convertidas} imágenes convertidas exitosamente')
            )
        
        if total_errores > 0:
            self.stdout.write(
                self.style.ERROR(f'❌ {total_errores} errores encontrados')
            )
    
    def _procesar_modelo(self, modelo, campo_imagen, dry_run):
        """
        Procesa las imágenes de un modelo específico.
        
        Args:
            modelo: Clase del modelo de Django.
            campo_imagen: Nombre del campo de imagen.
            dry_run: Si es True, solo muestra información sin modificar.
        
        Returns:
            tuple: (cantidad_convertidas, cantidad_errores)
        """
        convertidas = 0
        errores = 0
        archivos_a_eliminar = []  # Lista de archivos antiguos para eliminar al final
        
        objetos = modelo.objects.all()
        total = objetos.count()
        
        self.stdout.write(f'   Encontrados: {total} registros')
        
        for obj in objetos:
            imagen = getattr(obj, campo_imagen)
            
            if not imagen:
                continue
            
            if not necesita_conversion(imagen):
                self.stdout.write(
                    f'   ⏭️  {imagen.name} - Ya es WebP'
                )
                continue
            
            try:
                # Guardar ruta del archivo antiguo para eliminarlo después
                ruta_antigua = imagen.path if imagen else None
                nombre_antiguo = os.path.basename(imagen.name) if imagen else None
                
                if dry_run:
                    self.stdout.write(
                        f'   🔄 {imagen.name} → .webp (dry-run)'
                    )
                    convertidas += 1
                else:
                    # Convertir la imagen
                    nuevo_contenido, nuevo_nombre = procesar_imagen(imagen)
                    
                    # Cerrar el archivo de imagen para liberar el bloqueo
                    imagen.close()
                    
                    # Guardar nueva imagen
                    getattr(obj, campo_imagen).save(
                        nuevo_nombre, 
                        nuevo_contenido, 
                        save=False
                    )
                    obj.save()
                    
                    # Agregar archivo antiguo a la lista para eliminar después
                    if ruta_antigua:
                        nueva_ruta = getattr(obj, campo_imagen).path
                        if ruta_antigua != nueva_ruta and os.path.exists(ruta_antigua):
                            archivos_a_eliminar.append(ruta_antigua)
                    
                    self.stdout.write(
                        f'   ✅ {nombre_antiguo} → {nuevo_nombre}'
                    )
                    convertidas += 1
                    
            except Exception as e:
                errores += 1
                self.stdout.write(
                    self.style.ERROR(f'   ❌ Error en {imagen.name}: {str(e)}')
                )
        
        # Eliminar archivos antiguos al final
        for ruta in archivos_a_eliminar:
            try:
                os.remove(ruta)
            except Exception as e:
                self.stdout.write(
                    self.style.WARNING(f'   ⚠️  No se pudo eliminar {ruta}: {str(e)}')
                )
        
        return convertidas, errores
