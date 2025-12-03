"""
Configuración del panel de administración para el catálogo de productos.

Este módulo configura la interfaz de administración de Django para gestionar
categorías, marcas, productos, presentaciones e imágenes de manera eficiente.
"""

from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Categoria, Marca, Producto, Presentacion, 
    ImagenProducto, VideoProducto, EspecificacionProducto
)


class ImagenProductoInline(admin.TabularInline):
    """
    Inline para gestionar las imágenes de un producto.
    
    Permite agregar, editar y eliminar imágenes directamente desde
    la página de edición del producto. Una imagen puede marcarse como principal.
    """
    model = ImagenProducto
    extra = 1
    fields = ['imagen', 'titulo', 'es_principal', 'mostrar_en_galeria', 'mostrar_en_descripcion', 'orden']
    readonly_fields = ['mostrar_preview']
    
    def mostrar_preview(self, obj):
        """Muestra una miniatura de la imagen."""
        if obj.imagen:
            return format_html(
                '<img src="{}" width="100" height="100" style="object-fit: cover; border-radius: 5px;" />',
                obj.imagen.url
            )
        return '-'
    mostrar_preview.short_description = 'Vista previa'


class VideoProductoInline(admin.TabularInline):
    """
    Inline para gestionar los videos de un producto.
    
    Permite agregar videos de YouTube al producto.
    """
    model = VideoProducto
    extra = 0
    fields = ['titulo', 'url_youtube', 'orden']
    verbose_name = 'Video'
    verbose_name_plural = 'Videos'


class EspecificacionProductoInline(admin.TabularInline):
    """
    Inline para gestionar las especificaciones técnicas de un producto.
    
    Permite agregar especificaciones con nombre y valor.
    """
    model = EspecificacionProducto
    extra = 0
    fields = ['nombre', 'valor', 'orden']
    verbose_name = 'Especificación técnica'
    verbose_name_plural = 'Especificaciones técnicas'


class PresentacionInline(admin.TabularInline):
    """
    Inline para gestionar las presentaciones de un producto.
    
    Permite agregar, editar y eliminar presentaciones (tamaños, versiones)
    directamente desde la página de edición del producto.
    """
    model = Presentacion
    extra = 1
    fields = ['nombre', 'sku', 'precio', 'precio_oferta', 'stock', 'activo', 'orden']
    show_change_link = True


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    """
    Configuración del admin para el modelo Categoría.
    
    Proporciona una interfaz completa para gestionar las categorías
    de productos con funcionalidades de búsqueda y filtrado.
    Soporta jerarquía de categorías padre-hijo (subcategorías).
    """
    
    list_display = [
        'mostrar_nombre_jerarquico', 'slug', 'mostrar_imagen', 
        'mostrar_categoria_padre', 'mostrar_subcategorias_count',
        'activo', 'orden', 'fecha_creacion'
    ]
    list_display_links = ['mostrar_nombre_jerarquico']
    list_editable = ['activo', 'orden']
    list_filter = ['activo', 'categoria_padre', 'fecha_creacion']
    search_fields = ['nombre', 'descripcion']
    prepopulated_fields = {'slug': ('nombre',)}
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion', 'mostrar_imagen_grande', 'mostrar_ruta_completa']
    ordering = ['categoria_padre__nombre', 'orden', 'nombre']
    autocomplete_fields = ['categoria_padre']
    
    fieldsets = (
        ('Información Principal', {
            'fields': ('nombre', 'slug', 'descripcion')
        }),
        ('Jerarquía', {
            'fields': ('categoria_padre', 'mostrar_ruta_completa'),
            'description': 'Deja vacío "Categoría padre" para crear una categoría principal. '
                          'Selecciona una categoría padre para crear una subcategoría.'
        }),
        ('Imagen', {
            'fields': ('imagen', 'mostrar_imagen_grande')
        }),
        ('Configuración', {
            'fields': ('activo', 'orden')
        }),
        ('Información del Sistema', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
    
    def mostrar_imagen(self, obj):
        """Muestra una miniatura de la imagen en el listado."""
        if obj.imagen:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 5px;" />',
                obj.imagen.url
            )
        return '-'
    mostrar_imagen.short_description = 'Imagen'
    
    def mostrar_imagen_grande(self, obj):
        """Muestra la imagen en tamaño grande en el formulario de edición."""
        if obj.imagen:
            return format_html(
                '<img src="{}" width="200" style="border-radius: 10px;" />',
                obj.imagen.url
            )
        return 'Sin imagen'
    mostrar_imagen_grande.short_description = 'Vista previa'
    
    def mostrar_nombre_jerarquico(self, obj):
        """Muestra el nombre con indentación visual según nivel de jerarquía."""
        if obj.categoria_padre:
            return format_html(
                '<span style="color: #666; margin-right: 5px;">↳</span> {}',
                obj.nombre
            )
        return format_html('<strong>{}</strong>', obj.nombre)
    mostrar_nombre_jerarquico.short_description = 'Nombre'
    mostrar_nombre_jerarquico.admin_order_field = 'nombre'
    
    def mostrar_categoria_padre(self, obj):
        """Muestra la categoría padre o indica si es principal."""
        if obj.categoria_padre:
            return obj.categoria_padre.nombre
        return format_html('<span style="color: #28a745; font-weight: bold;">Principal</span>')
    mostrar_categoria_padre.short_description = 'Categoría padre'
    mostrar_categoria_padre.admin_order_field = 'categoria_padre__nombre'
    
    def mostrar_subcategorias_count(self, obj):
        """Muestra la cantidad de subcategorías activas."""
        count = obj.subcategorias.filter(activo=True).count()
        if count > 0:
            return format_html(
                '<span style="background: #17a2b8; color: white; padding: 2px 8px; border-radius: 10px;">{}</span>',
                count
            )
        return '-'
    mostrar_subcategorias_count.short_description = 'Subcategorías'
    
    def mostrar_ruta_completa(self, obj):
        """Muestra la ruta jerárquica completa de la categoría."""
        if obj.pk:
            return obj.obtener_ruta_completa()
        return 'Se mostrará después de guardar'
    mostrar_ruta_completa.short_description = 'Ruta completa'


@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    """
    Configuración del admin para el modelo Marca.
    
    Proporciona una interfaz para gestionar las marcas de productos.
    """
    
    list_display = ['nombre', 'slug', 'mostrar_logo', 'activo']
    list_display_links = ['nombre']
    list_editable = ['activo']
    list_filter = ['activo']
    search_fields = ['nombre', 'descripcion']
    prepopulated_fields = {'slug': ('nombre',)}
    ordering = ['nombre']
    
    fieldsets = (
        ('Información Principal', {
            'fields': ('nombre', 'slug', 'descripcion')
        }),
        ('Logo', {
            'fields': ('logo',)
        }),
        ('Configuración', {
            'fields': ('activo',)
        }),
    )
    
    def mostrar_logo(self, obj):
        """Muestra una miniatura del logo en el listado."""
        if obj.logo:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: contain; border-radius: 5px;" />',
                obj.logo.url
            )
        return '-'
    mostrar_logo.short_description = 'Logo'


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    """
    Configuración del admin para el modelo Producto.
    
    Proporciona una interfaz completa para gestionar los productos
    con funcionalidades avanzadas de búsqueda, filtrado y edición en línea.
    Los precios y stock se gestionan a través de las presentaciones.
    Las imágenes se gestionan a través del inline de Imágenes de Productos.
    """
    
    class Media:
        """Archivos CSS adicionales para el admin de Producto."""
        css = {
            'all': ('css/admin_ckeditor_dark.css',)
        }
    
    list_display = [
        'nombre', 'categoria', 'marca', 'modelo', 'mostrar_imagen',
        'mostrar_precio_desde', 'mostrar_presentaciones', 'mostrar_imagenes', 'activo', 'destacado'
    ]
    list_display_links = ['nombre']
    list_editable = ['activo', 'destacado']
    list_filter = ['categoria', 'marca', 'activo', 'destacado', 'fecha_creacion']
    search_fields = ['nombre', 'descripcion', 'modelo', 'marca__nombre']
    prepopulated_fields = {'slug': ('nombre',)}
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    autocomplete_fields = ['categoria', 'marca']
    ordering = ['-fecha_creacion']
    list_per_page = 25
    
    inlines = [ImagenProductoInline, PresentacionInline, EspecificacionProductoInline, VideoProductoInline]
    
    fieldsets = (
        ('Información Principal', {
            'fields': ('categoria', 'marca', 'nombre', 'modelo', 'slug')
        }),
        ('Descripción Corta', {
            'fields': ('descripcion_corta',),
            'description': 'Esta descripción se muestra junto a la imagen principal del producto.'
        }),
        ('Descripción Detallada', {
            'fields': ('descripcion',),
            'description': 'Esta descripción se muestra en la parte inferior del producto. Puedes agregar formato, imágenes y más.'
        }),
        ('Configuración', {
            'fields': ('activo', 'destacado')
        }),
        ('Información del Sistema', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
    
    def mostrar_imagen(self, obj):
        """Muestra una miniatura de la imagen principal en el listado."""
        imagen_url = obj.imagen_principal_url
        if imagen_url:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 5px;" />',
                imagen_url
            )
        return format_html('<span style="color: #999;"><i>Sin imagen</i></span>')
    mostrar_imagen.short_description = 'Imagen'
    
    def mostrar_imagenes(self, obj):
        """Muestra el número de imágenes del producto."""
        count = obj.imagenes.count()
        tiene_principal = obj.imagenes.filter(es_principal=True).exists()
        if count > 0:
            color = '#28a745' if tiene_principal else '#ffc107'
            icono = '✓' if tiene_principal else '!'
            return format_html(
                '<span style="background-color: {}; color: white; padding: 2px 8px; border-radius: 10px;">{} {}</span>',
                color, count, icono
            )
        return format_html(
            '<span style="background-color: #dc3545; color: white; padding: 2px 8px; border-radius: 10px;">0</span>'
        )
    mostrar_imagenes.short_description = 'Imágenes'
    
    def mostrar_precio_desde(self, obj):
        """Muestra el precio más bajo de las presentaciones."""
        precio = obj.precio_desde
        if precio:
            return format_html('<strong>Desde ${}</strong>', precio)
        return '-'
    mostrar_precio_desde.short_description = 'Precio'
    
    def mostrar_presentaciones(self, obj):
        """Muestra el número de presentaciones del producto."""
        count = obj.presentaciones.filter(activo=True).count()
        if count > 0:
            return format_html(
                '<span style="background-color: #28a745; color: white; padding: 2px 8px; border-radius: 10px;">{}</span>',
                count
            )
        return format_html(
            '<span style="background-color: #dc3545; color: white; padding: 2px 8px; border-radius: 10px;">0</span>'
        )
    mostrar_presentaciones.short_description = 'Presentaciones'


@admin.register(Presentacion)
class PresentacionAdmin(admin.ModelAdmin):
    """
    Configuración del admin para el modelo Presentación.
    
    Permite gestionar las presentaciones de productos de forma independiente.
    """
    
    list_display = [
        'producto', 'nombre', 'sku', 'mostrar_imagen', 
        'precio', 'precio_oferta', 'stock', 'activo', 'orden'
    ]
    list_display_links = ['producto', 'nombre']
    list_editable = ['precio', 'precio_oferta', 'stock', 'activo', 'orden']
    list_filter = ['producto__categoria', 'producto__marca', 'activo']
    search_fields = ['producto__nombre', 'nombre', 'sku']
    ordering = ['producto', 'orden']
    list_per_page = 50
    
    fieldsets = (
        ('Producto', {
            'fields': ('producto',)
        }),
        ('Información de la Presentación', {
            'fields': ('nombre', 'sku', 'caracteristicas')
        }),
        ('Precios e Inventario', {
            'fields': ('precio', 'precio_oferta', 'stock')
        }),
        ('Configuración', {
            'fields': ('activo', 'orden')
        }),
    )
    
    def mostrar_imagen(self, obj):
        """Muestra una miniatura de la imagen del producto."""
        imagen_url = obj.producto.imagen_principal_url
        if imagen_url:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 5px;" />',
                imagen_url
            )
        return '-'
    mostrar_imagen.short_description = 'Imagen'


@admin.register(ImagenProducto)
class ImagenProductoAdmin(admin.ModelAdmin):
    """
    Configuración del admin para el modelo ImagenProducto.
    
    Permite gestionar las imágenes de productos de forma independiente.
    """
    
    list_display = ['producto', 'titulo', 'mostrar_imagen', 'es_principal', 'mostrar_en_galeria', 'mostrar_en_descripcion', 'orden']
    list_display_links = ['producto', 'titulo']
    list_editable = ['es_principal', 'mostrar_en_galeria', 'mostrar_en_descripcion', 'orden']
    list_filter = ['producto__categoria', 'es_principal', 'mostrar_en_galeria', 'mostrar_en_descripcion']
    search_fields = ['producto__nombre', 'titulo']
    ordering = ['producto', '-es_principal', 'orden']
    
    def mostrar_imagen(self, obj):
        """Muestra una miniatura de la imagen en el listado."""
        if obj.imagen:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 5px;" />',
                obj.imagen.url
            )
        return '-'
    mostrar_imagen.short_description = 'Imagen'


@admin.register(VideoProducto)
class VideoProductoAdmin(admin.ModelAdmin):
    """
    Configuración del admin para el modelo VideoProducto.
    
    Permite gestionar los videos de productos.
    """
    
    list_display = ['producto', 'titulo', 'url_youtube', 'orden']
    list_display_links = ['producto', 'titulo']
    list_editable = ['orden']
    list_filter = ['producto__categoria']
    search_fields = ['producto__nombre', 'titulo']
    ordering = ['producto', 'orden']


@admin.register(EspecificacionProducto)
class EspecificacionProductoAdmin(admin.ModelAdmin):
    """
    Configuración del admin para el modelo EspecificacionProducto.
    
    Permite gestionar las especificaciones técnicas de productos.
    """
    
    list_display = ['producto', 'nombre', 'valor', 'orden']
    list_display_links = ['producto', 'nombre']
    list_editable = ['valor', 'orden']
    list_filter = ['producto__categoria']
    search_fields = ['producto__nombre', 'nombre', 'valor']
    ordering = ['producto', 'orden']


# Personalización del sitio de administración
admin.site.site_header = 'GardenAqua - Panel de Administración'
admin.site.site_title = 'GardenAqua Admin'
admin.site.index_title = 'Bienvenido al Panel de Administración de GardenAqua'
