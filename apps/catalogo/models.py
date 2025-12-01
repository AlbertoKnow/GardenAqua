"""
Modelos del catálogo de productos de GardenAqua.

Este módulo contiene los modelos principales para gestionar el catálogo
de productos de la tienda, incluyendo categorías y productos.
"""

from django.db import models
from django.urls import reverse
from slugify import slugify


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
    
    def save(self, *args, **kwargs):
        """
        Sobrescribe el método save para generar el slug automáticamente.
        
        Si no se proporciona un slug, se genera a partir del nombre
        usando la librería python-slugify.
        """
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        """Retorna la URL absoluta de la categoría."""
        return reverse('catalogo:categoria_detalle', kwargs={'slug': self.slug})


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
    
    def save(self, *args, **kwargs):
        """Genera el slug automáticamente a partir del nombre."""
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)


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
        descripcion (str): Descripción detallada del producto.
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
    descripcion = models.TextField(
        blank=True,
        verbose_name='Descripción',
        help_text='Descripción detallada del producto'
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
    
    def save(self, *args, **kwargs):
        """
        Sobrescribe el método save para generar el slug automáticamente.
        
        Si no se proporciona un slug, se genera a partir del nombre
        usando la librería python-slugify.
        """
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)
    
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
        ordering = ['orden', 'nombre']
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
    def disponible(self):
        """Indica si la presentación está disponible para compra."""
        return self.activo and self.stock > 0


class ImagenProducto(models.Model):
    """
    Modelo para imágenes de productos.
    
    Gestiona todas las imágenes de un producto en un solo lugar.
    Una imagen puede marcarse como principal para mostrarla en listados.
    
    Atributos:
        producto (ForeignKey): Producto al que pertenece la imagen.
        imagen (ImageField): Archivo de imagen.
        titulo (str): Título descriptivo de la imagen.
        es_principal (bool): Indica si es la imagen principal del producto.
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
        principal = " (Principal)" if self.es_principal else ""
        return f"Imagen de {self.producto.nombre}{principal}"
    
    def save(self, *args, **kwargs):
        """
        Sobrescribe save para asegurar que solo haya una imagen principal.
        
        Si esta imagen se marca como principal, desmarca las demás.
        """
        if self.es_principal:
            # Desmarcar otras imágenes principales del mismo producto
            ImagenProducto.objects.filter(
                producto=self.producto,
                es_principal=True
            ).exclude(pk=self.pk).update(es_principal=False)
        super().save(*args, **kwargs)

