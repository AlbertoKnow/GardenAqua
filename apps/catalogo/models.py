"""
Modelos del catálogo de productos de GardenAqua.

Este módulo contiene los modelos principales para gestionar el catálogo
de productos de la tienda, incluyendo categorías y productos.
"""

from django.db import models
from django.urls import reverse
from django.core.validators import URLValidator, MinValueValidator, MaxValueValidator
from slugify import slugify
from django_ckeditor_5.fields import CKEditor5Field

from .utils import procesar_imagen, necesita_conversion


class Categoria(models.Model):
    """
    Modelo para las categorías de productos.
    
    Representa las diferentes categorías de productos disponibles en la tienda,
    como peces, acuarios, alimentos, accesorios, etc.
    
    Atributos:
        nombre (str): Nombre de la categoría.
        slug (str): Identificador único para URL amigable.
        descripcion (str): Descripción detallada de la categoría.
        imagen (ImageField): Imagen representativa de la categoría.
        activo (bool): Indica si la categoría está activa en la tienda.
        orden (int): Orden de visualización de la categoría.
        fecha_creacion (datetime): Fecha de creación del registro.
        fecha_actualizacion (datetime): Fecha de última actualización.
    """
    
    nombre = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Nombre',
        help_text='Nombre de la categoría'
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        blank=True,
        verbose_name='Slug',
        help_text='Identificador único para URL (se genera automáticamente)'
    )
    descripcion = models.TextField(
        blank=True,
        verbose_name='Descripción',
        help_text='Descripción detallada de la categoría'
    )
    imagen = models.ImageField(
        upload_to='categorias/',
        blank=True,
        null=True,
        verbose_name='Imagen',
        help_text='Imagen representativa de la categoría'
    )
    activo = models.BooleanField(
        default=True,
        verbose_name='Activo',
        help_text='Indica si la categoría está visible en la tienda'
    )
    categoria_padre = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subcategorias',
        verbose_name='Categoría padre',
        help_text='Categoría padre para crear subcategorías (dejar vacío si es categoría principal)'
    )
    orden = models.PositiveIntegerField(
        default=0,
        verbose_name='Orden',
        help_text='Orden de visualización (menor número = mayor prioridad)'
    )
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación'
    )
    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        verbose_name='Fecha de actualización'
    )
    
    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['orden', 'nombre']
    
    def __str__(self):
        """Retorna el nombre de la categoría como representación en cadena."""
        return self.nombre
    
    def __init__(self, *args, **kwargs):
        """Guarda el nombre original para detectar cambios."""
        super().__init__(*args, **kwargs)
        self._nombre_original = self.nombre
    
    def save(self, *args, **kwargs):
        """
        Sobrescribe el método save para generar el slug automáticamente
        y convertir la imagen a WebP.
        
        El slug se genera o actualiza cuando:
        - No existe slug (nuevo registro)
        - El nombre ha cambiado
        """
        # Regenerar slug si es nuevo o si cambió el nombre
        if not self.slug or self.nombre != self._nombre_original:
            self.slug = slugify(self.nombre)
        
        # Convertir imagen a WebP si es necesario
        if self.imagen and necesita_conversion(self.imagen):
            nuevo_contenido, nuevo_nombre = procesar_imagen(self.imagen)
            self.imagen.save(nuevo_nombre, nuevo_contenido, save=False)
        
        super().save(*args, **kwargs)
        # Actualizar nombre original después de guardar
        self._nombre_original = self.nombre
    
    def get_absolute_url(self):
        """Retorna la URL absoluta de la categoría."""
        return reverse('catalogo:categoria_detalle', kwargs={'slug': self.slug})
    
    @property
    def es_categoria_principal(self):
        """
        Indica si la categoría es principal (no tiene padre).
        
        Returns:
            bool: True si es categoría principal, False si es subcategoría.
        """
        return self.categoria_padre is None
    
    @property
    def tiene_subcategorias(self):
        """
        Indica si la categoría tiene subcategorías.
        
        Returns:
            bool: True si tiene subcategorías activas.
        """
        return self.subcategorias.filter(activo=True).exists()
    
    def obtener_subcategorias_activas(self):
        """
        Obtiene todas las subcategorías activas de esta categoría.
        
        Returns:
            QuerySet: Subcategorías activas ordenadas.
        """
        return self.subcategorias.filter(activo=True).order_by('orden', 'nombre')
    
    def obtener_ruta_completa(self):
        """
        Obtiene la ruta completa de la categoría (ej: "Plantas > Plantas de Fondo").
        
        Returns:
            str: Ruta completa de la categoría.
        """
        if self.categoria_padre:
            return f"{self.categoria_padre.obtener_ruta_completa()} > {self.nombre}"
        return self.nombre
    
    def obtener_todas_subcategorias(self):
        """
        Obtiene recursivamente todas las subcategorías (hijas, nietas, etc.).
        
        Returns:
            list: Lista de todas las subcategorías.
        """
        resultado = []
        for subcategoria in self.subcategorias.filter(activo=True):
            resultado.append(subcategoria)
            resultado.extend(subcategoria.obtener_todas_subcategorias())
        return resultado
    
    def obtener_todos_productos(self):
        """
        Obtiene todos los productos de esta categoría y sus subcategorías.
        
        Returns:
            QuerySet: Productos de esta categoría y subcategorías.
        """
        from django.db.models import Q
        
        # Incluir esta categoría y todas sus subcategorías
        categorias_ids = [self.id]
        for sub in self.obtener_todas_subcategorias():
            categorias_ids.append(sub.id)
        
        return Producto.objects.filter(
            categoria_id__in=categorias_ids,
            activo=True
        )


class Marca(models.Model):
    """
    Modelo para las marcas de productos.
    
    Representa las diferentes marcas de productos disponibles en la tienda.
    
    Atributos:
        nombre (str): Nombre de la marca.
        slug (str): Identificador único para URL amigable.
        logo (ImageField): Logo de la marca.
        descripcion (str): Descripción de la marca.
        activo (bool): Indica si la marca está activa.
    """
    
    nombre = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Nombre',
        help_text='Nombre de la marca'
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        blank=True,
        verbose_name='Slug',
        help_text='Identificador único para URL (se genera automáticamente)'
    )
    logo = models.ImageField(
        upload_to='marcas/',
        blank=True,
        null=True,
        verbose_name='Logo',
        help_text='Logo de la marca'
    )
    descripcion = models.TextField(
        blank=True,
        verbose_name='Descripción',
        help_text='Descripción de la marca'
    )
    activo = models.BooleanField(
        default=True,
        verbose_name='Activo',
        help_text='Indica si la marca está visible en la tienda'
    )
    
    class Meta:
        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas'
        ordering = ['nombre']
    
    def __str__(self):
        """Retorna el nombre de la marca como representación en cadena."""
        return self.nombre
    
    def __init__(self, *args, **kwargs):
        """Guarda el nombre original para detectar cambios."""
        super().__init__(*args, **kwargs)
        self._nombre_original = self.nombre
    
    def save(self, *args, **kwargs):
        """
        Genera el slug automáticamente y convierte el logo a WebP.
        
        El slug se regenera si el nombre ha cambiado.
        """
        # Regenerar slug si es nuevo o si cambió el nombre
        if not self.slug or self.nombre != self._nombre_original:
            self.slug = slugify(self.nombre)
        
        # Convertir logo a WebP si es necesario
        if self.logo and necesita_conversion(self.logo):
            nuevo_contenido, nuevo_nombre = procesar_imagen(self.logo)
            self.logo.save(nuevo_nombre, nuevo_contenido, save=False)
        
        super().save(*args, **kwargs)
        # Actualizar nombre original después de guardar
        self._nombre_original = self.nombre


class Producto(models.Model):
    """
    Modelo para los productos de la tienda.
    
    Representa los productos base disponibles para venta en GardenAqua.
    Cada producto puede tener múltiples presentaciones con diferentes
    tamaños, precios y características.
    
    Atributos:
        categoria (ForeignKey): Categoría a la que pertenece el producto.
        marca (ForeignKey): Marca del producto.
        nombre (str): Nombre del producto.
        modelo (str): Modelo o referencia del producto.
        slug (str): Identificador único para URL amigable.
        descripcion_corta (str): Descripción breve para listados.
        descripcion (str): Descripción detallada del producto (HTML).
        activo (bool): Indica si el producto está activo para venta.
        destacado (bool): Indica si el producto está destacado.
        fecha_creacion (datetime): Fecha de creación del registro.
        fecha_actualizacion (datetime): Fecha de última actualización.
    
    Nota:
        Las imágenes del producto se gestionan a través del modelo ImagenProducto.
        La imagen principal se determina por el campo es_principal de ImagenProducto.
    """
    
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        related_name='productos',
        verbose_name='Categoría',
        help_text='Categoría a la que pertenece el producto'
    )
    marca = models.ForeignKey(
        Marca,
        on_delete=models.SET_NULL,
        related_name='productos',
        verbose_name='Marca',
        help_text='Marca del producto',
        blank=True,
        null=True
    )
    nombre = models.CharField(
        max_length=200,
        verbose_name='Nombre',
        help_text='Nombre del producto'
    )
    modelo = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Modelo',
        help_text='Modelo o referencia del producto'
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        blank=True,
        verbose_name='Slug',
        help_text='Identificador único para URL (se genera automáticamente)'
    )
    descripcion_corta = models.TextField(
        max_length=500,
        blank=True,
        verbose_name='Descripción corta',
        help_text='Descripción breve del producto (máx. 500 caracteres). Se muestra junto a la imagen principal.'
    )
    descripcion = CKEditor5Field(
        blank=True,
        verbose_name='Descripción detallada',
        help_text='Descripción completa del producto con formato. Se muestra en la sección inferior.',
        config_name='extends'
    )
    activo = models.BooleanField(
        default=True,
        verbose_name='Activo',
        help_text='Indica si el producto está disponible para venta'
    )
    destacado = models.BooleanField(
        default=False,
        verbose_name='Destacado',
        help_text='Indica si el producto aparece en la sección de destacados'
    )
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación'
    )
    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        verbose_name='Fecha de actualización'
    )
    
    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['-fecha_creacion']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['categoria']),
            models.Index(fields=['activo', 'destacado']),
        ]
    
    def __str__(self):
        """Retorna el nombre del producto como representación en cadena."""
        if self.marca:
            return f"{self.nombre} - {self.marca.nombre}"
        return self.nombre
    
    def __init__(self, *args, **kwargs):
        """Guarda el nombre original para detectar cambios."""
        super().__init__(*args, **kwargs)
        self._nombre_original = self.nombre
    
    def save(self, *args, **kwargs):
        """
        Sobrescribe el método save para generar el slug automáticamente.
        
        El slug se genera o actualiza cuando:
        - No existe slug (nuevo registro)
        - El nombre ha cambiado
        """
        # Regenerar slug si es nuevo o si cambió el nombre
        if not self.slug or self.nombre != self._nombre_original:
            self.slug = slugify(self.nombre)
        
        super().save(*args, **kwargs)
        # Actualizar nombre original después de guardar
        self._nombre_original = self.nombre
    
    def get_absolute_url(self):
        """Retorna la URL absoluta del producto."""
        return reverse('catalogo:producto_detalle', kwargs={'slug': self.slug})
    
    @property
    def precio_desde(self):
        """
        Retorna el precio más bajo entre todas las presentaciones activas.
        
        Útil para mostrar "Desde $X" en listados de productos.
        """
        presentaciones = self.presentaciones.filter(activo=True)
        if presentaciones.exists():
            precios = []
            for p in presentaciones:
                precios.append(p.precio_actual)
            return min(precios)
        return None
    
    @property
    def tiene_oferta(self):
        """
        Indica si al menos una presentación tiene precio de oferta.
        """
        return self.presentaciones.filter(
            activo=True, 
            precio_oferta__isnull=False
        ).exists()
    
    @property
    def tiene_stock(self):
        """Indica si al menos una presentación tiene stock disponible."""
        return self.presentaciones.filter(activo=True, stock__gt=0).exists()
    
    @property
    def presentacion_principal(self):
        """
        Retorna la presentación principal del producto.
        
        Busca la primera presentación activa con stock disponible,
        ordenada por precio (menor primero).
        
        Returns:
            Presentacion: Primera presentación activa con stock o None.
        """
        # Buscar presentación activa con stock, ordenada por precio
        presentacion = self.presentaciones.filter(
            activo=True, 
            stock__gt=0
        ).order_by('precio').first()
        
        if presentacion:
            return presentacion
        
        # Si no hay con stock, retornar cualquier presentación activa
        return self.presentaciones.filter(activo=True).order_by('precio').first()
    
    @property
    def disponible(self):
        """Indica si el producto está disponible para compra."""
        return self.activo and self.tiene_stock
    
    @property
    def imagen_principal_url(self):
        """
        Retorna la URL de la imagen principal del producto.
        
        Busca primero en las imágenes marcadas como principal (es_principal=True),
        si no hay ninguna marcada, usa la primera imagen de la galería.
        
        Returns:
            str: URL de la imagen o None si no hay imágenes.
        """
        # Buscar imagen marcada como principal
        imagen_principal = self.imagenes.filter(es_principal=True).first()
        if imagen_principal:
            return imagen_principal.imagen.url
        
        # Usar primera imagen de la galería (ordenada por orden)
        primera_imagen = self.imagenes.first()
        if primera_imagen:
            return primera_imagen.imagen.url
        
        return None
    
    @property
    def imagen_principal_obj(self):
        """
        Retorna el objeto ImagenProducto marcado como principal.
        
        Returns:
            ImagenProducto: Imagen principal o primera imagen disponible.
        """
        imagen = self.imagenes.filter(es_principal=True).first()
        if imagen:
            return imagen
        return self.imagenes.first()
    
    @property
    def todas_las_imagenes(self):
        """
        Retorna todas las imágenes del producto ordenadas.
        
        Incluye la imagen principal del modelo si existe y no está
        duplicada en la galería.
        """
        return self.imagenes.all()
    
    @property
    def imagenes_galeria(self):
        """
        Retorna las imágenes que deben mostrarse en la galería principal.
        """
        return self.imagenes.filter(mostrar_en_galeria=True)
    
    @property
    def imagenes_descripcion(self):
        """
        Retorna las imágenes que deben mostrarse en la descripción larga.
        """
        return self.imagenes.filter(mostrar_en_descripcion=True)
    
    @property
    def tiene_videos(self):
        """Indica si el producto tiene videos asociados."""
        return self.videos.exists()
    
    @property
    def tiene_especificaciones(self):
        """Indica si el producto tiene especificaciones técnicas."""
        return self.especificaciones.exists()


class Presentacion(models.Model):
    """
    Modelo para las presentaciones de un producto.
    
    Permite definir diferentes versiones de un mismo producto con
    sus propios precios, stock, imágenes y características.
    
    Ejemplos:
        - Alimento para peces: 100ml, 250ml, 500ml, 1000ml
        - Lámpara de acuario: 30cm, 50cm, 80cm, 120cm
        - Filtro: Modelo básico, Modelo pro, Modelo premium
    
    Atributos:
        producto (ForeignKey): Producto al que pertenece la presentación.
        nombre (str): Nombre de la presentación (ej: "100ml", "30cm").
        sku (str): Código único de identificación.
        precio (Decimal): Precio de venta.
        precio_oferta (Decimal): Precio con descuento (opcional).
        stock (int): Cantidad disponible en inventario.
        imagen (ImageField): Imagen específica de esta presentación.
        caracteristicas (TextField): Características específicas de la presentación.
        activo (bool): Indica si la presentación está activa.
        orden (int): Orden de visualización.
    """
    
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name='presentaciones',
        verbose_name='Producto'
    )
    nombre = models.CharField(
        max_length=100,
        verbose_name='Presentación',
        help_text='Nombre de la presentación (ej: 100ml, 30cm, Pack de 3)'
    )
    sku = models.CharField(
        max_length=50,
        unique=True,
        blank=True,
        null=True,
        verbose_name='SKU',
        help_text='Código único de identificación'
    )
    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Precio',
        help_text='Precio de venta'
    )
    precio_oferta = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name='Precio de oferta',
        help_text='Precio con descuento (dejar vacío si no hay oferta)'
    )
    stock = models.PositiveIntegerField(
        default=0,
        verbose_name='Stock',
        help_text='Cantidad disponible en inventario'
    )
    caracteristicas = models.TextField(
        blank=True,
        verbose_name='Características',
        help_text='Características específicas de esta presentación'
    )
    activo = models.BooleanField(
        default=True,
        verbose_name='Activo',
        help_text='Indica si la presentación está disponible para venta'
    )
    orden = models.PositiveIntegerField(
        default=0,
        verbose_name='Orden',
        help_text='Orden de visualización'
    )
    
    class Meta:
        verbose_name = 'Presentación'
        verbose_name_plural = 'Presentaciones'
        ordering = ['precio']  # Ordenar por precio de menor a mayor
        unique_together = ['producto', 'nombre']
    
    def __str__(self):
        """Retorna una descripción de la presentación."""
        return f"{self.producto.nombre} - {self.nombre}"
    
    @property
    def precio_actual(self):
        """
        Retorna el precio actual de la presentación.
        
        Si existe un precio de oferta, retorna ese precio,
        de lo contrario retorna el precio regular.
        """
        if self.precio_oferta:
            return self.precio_oferta
        return self.precio
    
    @property
    def tiene_oferta(self):
        """Indica si la presentación tiene un precio de oferta activo."""
        return self.precio_oferta is not None
    
    @property
    def porcentaje_descuento(self):
        """
        Calcula el porcentaje de descuento.
        
        Returns:
            int: Porcentaje de descuento redondeado, o 0 si no hay oferta.
        """
        if self.tiene_oferta and self.precio > 0:
            descuento = ((self.precio - self.precio_oferta) / self.precio) * 100
            return round(descuento)
        return 0
    
    @property
    def disponible(self):
        """Indica si la presentación está disponible para compra."""
        return self.activo and self.stock > 0


class ImagenProducto(models.Model):
    """
    Modelo para imágenes de productos.
    
    Gestiona todas las imágenes de un producto en un solo lugar.
    Una imagen puede marcarse como principal y definir dónde se muestra.
    
    Atributos:
        producto (ForeignKey): Producto al que pertenece la imagen.
        imagen (ImageField): Archivo de imagen.
        titulo (str): Título descriptivo de la imagen.
        es_principal (bool): Indica si es la imagen principal del producto.
        mostrar_en_galeria (bool): Si aparece en la galería superior.
        mostrar_en_descripcion (bool): Si aparece en la descripción larga.
        orden (int): Orden de visualización en la galería.
    """
    
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name='imagenes',
        verbose_name='Producto'
    )
    imagen = models.ImageField(
        upload_to='productos/galeria/',
        verbose_name='Imagen'
    )
    titulo = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Título',
        help_text='Título descriptivo de la imagen (ej: Vista frontal, Detalle, etc.)'
    )
    es_principal = models.BooleanField(
        default=False,
        verbose_name='Imagen principal',
        help_text='Marcar como imagen principal del producto (se mostrará en listados)'
    )
    mostrar_en_galeria = models.BooleanField(
        default=True,
        verbose_name='Mostrar en galería',
        help_text='Mostrar esta imagen en la galería principal del producto'
    )
    mostrar_en_descripcion = models.BooleanField(
        default=False,
        verbose_name='Mostrar en descripción',
        help_text='Mostrar esta imagen en la sección de descripción detallada'
    )
    orden = models.PositiveIntegerField(
        default=0,
        verbose_name='Orden',
        help_text='Orden de visualización en la galería'
    )
    
    class Meta:
        verbose_name = 'Imagen de producto'
        verbose_name_plural = 'Imágenes de productos'
        ordering = ['-es_principal', 'orden']
    
    def __str__(self):
        """Retorna una descripción de la imagen."""
        ubicacion = []
        if self.mostrar_en_galeria:
            ubicacion.append("Galería")
        if self.mostrar_en_descripcion:
            ubicacion.append("Descripción")
        ubicacion_str = " + ".join(ubicacion) if ubicacion else "Sin ubicación"
        principal = " ★" if self.es_principal else ""
        return f"{self.producto.nombre} - {ubicacion_str}{principal}"
    
    def save(self, *args, **kwargs):
        """
        Sobrescribe save para asegurar que solo haya una imagen principal
        y convertir la imagen a WebP.
        
        Si esta imagen se marca como principal, desmarca las demás.
        """
        # Convertir imagen a WebP si es necesario
        if self.imagen and necesita_conversion(self.imagen):
            nuevo_contenido, nuevo_nombre = procesar_imagen(self.imagen)
            self.imagen.save(nuevo_nombre, nuevo_contenido, save=False)
        
        if self.es_principal:
            # Desmarcar otras imágenes principales del mismo producto
            ImagenProducto.objects.filter(
                producto=self.producto,
                es_principal=True
            ).exclude(pk=self.pk).update(es_principal=False)
        super().save(*args, **kwargs)


class VideoProducto(models.Model):
    """
    Modelo para videos de productos.
    
    Permite asociar videos de YouTube a un producto para mostrar
    demostraciones, tutoriales, reseñas, etc.
    
    Atributos:
        producto (ForeignKey): Producto al que pertenece el video.
        titulo (str): Título descriptivo del video.
        url_youtube (str): URL del video de YouTube.
        orden (int): Orden de visualización.
    """
    
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name='videos',
        verbose_name='Producto'
    )
    titulo = models.CharField(
        max_length=200,
        verbose_name='Título',
        help_text='Título descriptivo del video'
    )
    url_youtube = models.URLField(
        verbose_name='URL de YouTube',
        help_text='URL completa del video de YouTube (ej: https://www.youtube.com/watch?v=xxxxx)',
        validators=[URLValidator()]
    )
    orden = models.PositiveIntegerField(
        default=0,
        verbose_name='Orden',
        help_text='Orden de visualización'
    )
    
    class Meta:
        verbose_name = 'Video de producto'
        verbose_name_plural = 'Videos de productos'
        ordering = ['orden']
    
    def __str__(self):
        """Retorna el título del video."""
        return f"{self.producto.nombre} - {self.titulo}"
    
    @property
    def youtube_id(self):
        """
        Extrae el ID del video de YouTube desde la URL.
        
        Soporta formatos:
        - https://www.youtube.com/watch?v=VIDEO_ID
        - https://youtu.be/VIDEO_ID
        - https://www.youtube.com/embed/VIDEO_ID
        """
        import re
        patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)',
        ]
        for pattern in patterns:
            match = re.search(pattern, self.url_youtube)
            if match:
                return match.group(1)
        return None
    
    @property
    def embed_url(self):
        """Retorna la URL de embed para el iframe."""
        video_id = self.youtube_id
        if video_id:
            return f"https://www.youtube.com/embed/{video_id}"
        return None


class EspecificacionProducto(models.Model):
    """
    Modelo para especificaciones técnicas de productos.
    
    Permite definir características técnicas variables para cada producto.
    Cada especificación tiene un nombre y un valor.
    
    Ejemplos:
        - Potencia: 110 GPH
        - Voltaje: 110V
        - Dimensiones: 20x15x25 cm
        - Material: Plástico ABS
    
    Atributos:
        producto (ForeignKey): Producto al que pertenece la especificación.
        nombre (str): Nombre de la especificación (ej: "Potencia").
        valor (str): Valor de la especificación (ej: "110 GPH").
        orden (int): Orden de visualización en la tabla.
    """
    
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name='especificaciones',
        verbose_name='Producto'
    )
    nombre = models.CharField(
        max_length=100,
        verbose_name='Especificación',
        help_text='Nombre de la especificación (ej: Potencia, Voltaje, Dimensiones)'
    )
    valor = models.CharField(
        max_length=200,
        verbose_name='Valor',
        help_text='Valor de la especificación (ej: 110 GPH, 110V, 20x15x25 cm)'
    )
    orden = models.PositiveIntegerField(
        default=0,
        verbose_name='Orden',
        help_text='Orden de visualización en la tabla de especificaciones'
    )
    
    class Meta:
        verbose_name = 'Especificación técnica'
        verbose_name_plural = 'Especificaciones técnicas'
        ordering = ['orden', 'nombre']
    
    def __str__(self):
        """Retorna nombre: valor."""
        return f"{self.nombre}: {self.valor}"