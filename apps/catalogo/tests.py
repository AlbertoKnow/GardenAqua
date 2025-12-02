"""
Pruebas unitarias para la aplicación de catálogo.

Este módulo contiene las pruebas para los modelos, vistas y
funcionalidades del catálogo de productos.
"""

from django.test import TestCase, Client
from django.urls import reverse
from decimal import Decimal

from .models import (
    Categoria,
    Marca,
    Producto,
    Presentacion,
    ImagenProducto,
    VideoProducto,
    EspecificacionProducto
)


class CategoriaModelTest(TestCase):
    """Pruebas para el modelo Categoria."""
    
    def setUp(self):
        """Configuración inicial para las pruebas."""
        self.categoria = Categoria.objects.create(
            nombre='Acuarios',
            descripcion='Categoría de acuarios'
        )
    
    def test_creacion_categoria(self):
        """Verifica que la categoría se crea correctamente."""
        self.assertEqual(self.categoria.nombre, 'Acuarios')
        self.assertTrue(self.categoria.activo)
    
    def test_slug_generado_automaticamente(self):
        """Verifica que el slug se genera automáticamente."""
        self.assertEqual(self.categoria.slug, 'acuarios')
    
    def test_str_representation(self):
        """Verifica la representación string del modelo."""
        self.assertEqual(str(self.categoria), 'Acuarios')


class MarcaModelTest(TestCase):
    """Pruebas para el modelo Marca."""
    
    def setUp(self):
        """Configuración inicial para las pruebas."""
        self.marca = Marca.objects.create(
            nombre='AquaClear',
            descripcion='Marca de filtros'
        )
    
    def test_creacion_marca(self):
        """Verifica que la marca se crea correctamente."""
        self.assertEqual(self.marca.nombre, 'AquaClear')
        self.assertTrue(self.marca.activo)
    
    def test_slug_generado_automaticamente(self):
        """Verifica que el slug se genera automáticamente."""
        self.assertEqual(self.marca.slug, 'aquaclear')


class ProductoModelTest(TestCase):
    """Pruebas para el modelo Producto."""
    
    def setUp(self):
        """Configuración inicial para las pruebas."""
        self.categoria = Categoria.objects.create(nombre='Filtros')
        self.marca = Marca.objects.create(nombre='AquaClear')
        self.producto = Producto.objects.create(
            nombre='Filtro AquaClear 50',
            categoria=self.categoria,
            marca=self.marca,
            descripcion_corta='Filtro de cascada para acuarios',
            descripcion='<p>Descripción larga del filtro</p>'
        )
    
    def test_creacion_producto(self):
        """Verifica que el producto se crea correctamente."""
        self.assertEqual(self.producto.nombre, 'Filtro AquaClear 50')
        self.assertTrue(self.producto.activo)
    
    def test_slug_generado_automaticamente(self):
        """Verifica que el slug se genera automáticamente."""
        self.assertEqual(self.producto.slug, 'filtro-aquaclear-50')
    
    def test_descripcion_corta(self):
        """Verifica que la descripción corta funciona correctamente."""
        self.assertEqual(
            self.producto.descripcion_corta, 
            'Filtro de cascada para acuarios'
        )
    
    def test_relacion_categoria(self):
        """Verifica la relación con la categoría."""
        self.assertEqual(self.producto.categoria.nombre, 'Filtros')
    
    def test_relacion_marca(self):
        """Verifica la relación con la marca."""
        self.assertEqual(self.producto.marca.nombre, 'AquaClear')


class PresentacionModelTest(TestCase):
    """Pruebas para el modelo Presentacion."""
    
    def setUp(self):
        """Configuración inicial para las pruebas."""
        self.categoria = Categoria.objects.create(nombre='Filtros')
        self.producto = Producto.objects.create(
            nombre='Filtro AquaClear',
            categoria=self.categoria
        )
        self.presentacion = Presentacion.objects.create(
            producto=self.producto,
            nombre='50 galones',
            precio=Decimal('150.00'),
            stock=10
        )
    
    def test_creacion_presentacion(self):
        """Verifica que la presentación se crea correctamente."""
        self.assertEqual(self.presentacion.nombre, '50 galones')
        self.assertEqual(self.presentacion.precio, Decimal('150.00'))
        self.assertEqual(self.presentacion.stock, 10)
    
    def test_disponibilidad(self):
        """Verifica la propiedad de disponibilidad."""
        self.assertTrue(self.presentacion.disponible)
        
        # Sin stock
        self.presentacion.stock = 0
        self.presentacion.save()
        self.assertFalse(self.presentacion.disponible)
    
    def test_precio_actual(self):
        """Verifica que el precio actual se calcula correctamente."""
        # Sin descuento
        self.assertEqual(self.presentacion.precio_actual, Decimal('150.00'))
        
        # Con descuento
        self.presentacion.precio_oferta = Decimal('120.00')
        self.presentacion.save()
        self.assertEqual(self.presentacion.precio_actual, Decimal('120.00'))
    
    def test_tiene_oferta(self):
        """Verifica la propiedad tiene_oferta."""
        # Sin oferta
        self.assertFalse(self.presentacion.tiene_oferta)
        
        # Con oferta
        self.presentacion.precio_oferta = Decimal('120.00')
        self.presentacion.save()
        self.assertTrue(self.presentacion.tiene_oferta)
    
    def test_porcentaje_descuento(self):
        """Verifica el cálculo del porcentaje de descuento."""
        # Sin oferta
        self.assertEqual(self.presentacion.porcentaje_descuento, 0)
        
        # Con 20% de descuento (150 -> 120)
        self.presentacion.precio_oferta = Decimal('120.00')
        self.presentacion.save()
        self.assertEqual(self.presentacion.porcentaje_descuento, 20)
        
        # Con 50% de descuento (150 -> 75)
        self.presentacion.precio_oferta = Decimal('75.00')
        self.presentacion.save()
        self.assertEqual(self.presentacion.porcentaje_descuento, 50)


class ImagenProductoModelTest(TestCase):
    """Pruebas para el modelo ImagenProducto."""
    
    def setUp(self):
        """Configuración inicial para las pruebas."""
        self.categoria = Categoria.objects.create(nombre='Filtros')
        self.producto = Producto.objects.create(
            nombre='Filtro Test',
            categoria=self.categoria
        )
    
    def test_configuracion_ubicacion_campos(self):
        """Verifica que los campos de ubicación existen en el modelo."""
        # Verificamos que el modelo tiene los campos correctos
        from django.db import models
        
        imagen_model = ImagenProducto
        fields = {f.name: f for f in imagen_model._meta.get_fields()}
        
        self.assertIn('mostrar_en_galeria', fields)
        self.assertIn('mostrar_en_descripcion', fields)
    
    def test_defaults_ubicacion(self):
        """Verifica los valores por defecto de ubicación."""
        # Verificar valores por defecto directamente del modelo
        mostrar_en_galeria_field = ImagenProducto._meta.get_field('mostrar_en_galeria')
        mostrar_en_descripcion_field = ImagenProducto._meta.get_field('mostrar_en_descripcion')
        
        self.assertTrue(mostrar_en_galeria_field.default)
        self.assertFalse(mostrar_en_descripcion_field.default)


class VideoProductoModelTest(TestCase):
    """Pruebas para el modelo VideoProducto."""
    
    def setUp(self):
        """Configuración inicial para las pruebas."""
        self.categoria = Categoria.objects.create(nombre='Filtros')
        self.producto = Producto.objects.create(
            nombre='Filtro Test',
            categoria=self.categoria
        )
    
    def test_creacion_video(self):
        """Verifica que el video se crea correctamente."""
        video = VideoProducto.objects.create(
            producto=self.producto,
            titulo='Video de demostración',
            url_youtube='https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            orden=1
        )
        self.assertEqual(video.titulo, 'Video de demostración')
        self.assertEqual(video.orden, 1)
    
    def test_youtube_id_formato_watch(self):
        """Verifica la extracción de ID de YouTube formato watch."""
        video = VideoProducto.objects.create(
            producto=self.producto,
            titulo='Test',
            url_youtube='https://www.youtube.com/watch?v=dQw4w9WgXcQ'
        )
        self.assertEqual(video.youtube_id, 'dQw4w9WgXcQ')
    
    def test_youtube_id_formato_short(self):
        """Verifica la extracción de ID de YouTube formato corto."""
        video = VideoProducto.objects.create(
            producto=self.producto,
            titulo='Test',
            url_youtube='https://youtu.be/dQw4w9WgXcQ'
        )
        self.assertEqual(video.youtube_id, 'dQw4w9WgXcQ')
    
    def test_youtube_id_formato_embed(self):
        """Verifica la extracción de ID de YouTube formato embed."""
        video = VideoProducto.objects.create(
            producto=self.producto,
            titulo='Test',
            url_youtube='https://www.youtube.com/embed/dQw4w9WgXcQ'
        )
        self.assertEqual(video.youtube_id, 'dQw4w9WgXcQ')
    
    def test_embed_url(self):
        """Verifica la generación de URL de embed."""
        video = VideoProducto.objects.create(
            producto=self.producto,
            titulo='Test',
            url_youtube='https://www.youtube.com/watch?v=dQw4w9WgXcQ'
        )
        self.assertEqual(
            video.embed_url, 
            'https://www.youtube.com/embed/dQw4w9WgXcQ'
        )
    
    def test_str_representation(self):
        """Verifica la representación string del modelo."""
        video = VideoProducto.objects.create(
            producto=self.producto,
            titulo='Demo',
            url_youtube='https://www.youtube.com/watch?v=dQw4w9WgXcQ'
        )
        self.assertEqual(str(video), 'Filtro Test - Demo')


class EspecificacionProductoModelTest(TestCase):
    """Pruebas para el modelo EspecificacionProducto."""
    
    def setUp(self):
        """Configuración inicial para las pruebas."""
        self.categoria = Categoria.objects.create(nombre='Filtros')
        self.producto = Producto.objects.create(
            nombre='Filtro Test',
            categoria=self.categoria
        )
    
    def test_creacion_especificacion(self):
        """Verifica que la especificación se crea correctamente."""
        spec = EspecificacionProducto.objects.create(
            producto=self.producto,
            nombre='Potencia',
            valor='110 GPH',
            orden=1
        )
        self.assertEqual(spec.nombre, 'Potencia')
        self.assertEqual(spec.valor, '110 GPH')
        self.assertEqual(spec.orden, 1)
    
    def test_str_representation(self):
        """Verifica la representación string del modelo."""
        spec = EspecificacionProducto.objects.create(
            producto=self.producto,
            nombre='Voltaje',
            valor='110V'
        )
        self.assertEqual(str(spec), 'Voltaje: 110V')
    
    def test_ordenamiento(self):
        """Verifica el ordenamiento de especificaciones."""
        spec2 = EspecificacionProducto.objects.create(
            producto=self.producto,
            nombre='Peso',
            valor='500g',
            orden=2
        )
        spec1 = EspecificacionProducto.objects.create(
            producto=self.producto,
            nombre='Potencia',
            valor='110 GPH',
            orden=1
        )
        
        especificaciones = list(self.producto.especificaciones.all())
        self.assertEqual(especificaciones[0], spec1)
        self.assertEqual(especificaciones[1], spec2)


class ProductoDetalleViewTest(TestCase):
    """Pruebas para la vista de detalle de producto."""
    
    def setUp(self):
        """Configuración inicial para las pruebas."""
        self.client = Client()
        self.categoria = Categoria.objects.create(nombre='Filtros')
        self.producto = Producto.objects.create(
            nombre='Filtro Test View',
            categoria=self.categoria,
            descripcion_corta='Descripción corta test',
            descripcion='<p>Descripción larga</p>'
        )
        self.presentacion = Presentacion.objects.create(
            producto=self.producto,
            nombre='Estándar',
            precio=Decimal('100.00'),
            stock=5
        )
        
    def test_vista_detalle_producto(self):
        """Verifica que la vista de detalle funciona correctamente."""
        url = reverse('catalogo:producto_detalle', kwargs={'slug': self.producto.slug})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Filtro Test View')
        self.assertContains(response, 'Descripción corta test')
    
    def test_contexto_incluye_especificaciones(self):
        """Verifica que las especificaciones se incluyen en el contexto."""
        EspecificacionProducto.objects.create(
            producto=self.producto,
            nombre='Potencia',
            valor='100W'
        )
        
        url = reverse('catalogo:producto_detalle', kwargs={'slug': self.producto.slug})
        response = self.client.get(url)
        
        self.assertIn('especificaciones', response.context)
        self.assertEqual(len(response.context['especificaciones']), 1)
    
    def test_contexto_incluye_videos(self):
        """Verifica que los videos se incluyen en el contexto."""
        VideoProducto.objects.create(
            producto=self.producto,
            titulo='Demo',
            url_youtube='https://www.youtube.com/watch?v=test123'
        )
        
        url = reverse('catalogo:producto_detalle', kwargs={'slug': self.producto.slug})
        response = self.client.get(url)
        
        self.assertIn('videos', response.context)
        self.assertEqual(len(response.context['videos']), 1)
    
    def test_contexto_incluye_imagenes_separadas(self):
        """Verifica que las imágenes se separan correctamente."""
        url = reverse('catalogo:producto_detalle', kwargs={'slug': self.producto.slug})
        response = self.client.get(url)
        
        self.assertIn('imagenes_galeria', response.context)
        self.assertIn('imagenes_descripcion', response.context)
