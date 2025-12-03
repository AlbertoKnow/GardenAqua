"""
Vistas del catálogo de productos de GardenAqua.

Este módulo contiene las vistas para mostrar el catálogo de productos,
filtrar por categorías y ver los detalles de cada producto.
"""

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from .models import (
    Categoria, 
    Marca, 
    Producto, 
    Presentacion, 
    VideoProducto, 
    EspecificacionProducto
)


class ProductoListView(ListView):
    """
    Vista para mostrar el listado de productos.
    
    Permite filtrar productos por categoría y muestra solo
    los productos activos que tienen al menos una presentación disponible.
    """
    model = Producto
    template_name = 'catalogo/producto_lista.html'
    context_object_name = 'productos'
    paginate_by = 12
    
    def get_queryset(self):
        """
        Obtiene los productos filtrados.
        
        Filtra por categoría si se proporciona el slug en la URL.
        Solo muestra productos activos con presentaciones activas.
        """
        queryset = Producto.objects.filter(
            activo=True,
            presentaciones__activo=True
        ).distinct().select_related('categoria', 'marca').prefetch_related('presentaciones')
        
        # Filtrar por categoría si se proporciona
        categoria_slug = self.kwargs.get('categoria_slug')
        if categoria_slug:
            queryset = queryset.filter(categoria__slug=categoria_slug)
        
        # Filtrar por marca si se proporciona
        marca_slug = self.request.GET.get('marca')
        if marca_slug:
            queryset = queryset.filter(marca__slug=marca_slug)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        """Agrega las categorías y marcas al contexto."""
        context = super().get_context_data(**kwargs)
        
        # Solo categorías principales (sin padre) con sus subcategorías
        context['categorias'] = Categoria.objects.filter(
            activo=True,
            categoria_padre__isnull=True
        ).prefetch_related('subcategorias')
        
        # Todas las marcas activas
        context['marcas'] = Marca.objects.filter(activo=True)
        
        # Categoría actual (si hay filtro)
        categoria_slug = self.kwargs.get('categoria_slug')
        if categoria_slug:
            context['categoria_actual'] = get_object_or_404(
                Categoria, slug=categoria_slug, activo=True
            )
        
        # Marca actual (si hay filtro)
        marca_slug = self.request.GET.get('marca')
        if marca_slug:
            context['marca_actual'] = Marca.objects.filter(
                slug=marca_slug, activo=True
            ).first()
        
        return context


class ProductoDetailView(DetailView):
    """
    Vista para mostrar el detalle de un producto.
    
    Muestra toda la información del producto incluyendo
    sus presentaciones, imágenes y características.
    """
    model = Producto
    template_name = 'catalogo/producto_detalle.html'
    context_object_name = 'producto'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        """Solo muestra productos activos."""
        return Producto.objects.filter(activo=True).select_related(
            'categoria', 'marca'
        ).prefetch_related(
            'presentaciones', 
            'imagenes', 
            'videos', 
            'especificaciones'
        )
    
    def get_context_data(self, **kwargs):
        """
        Agrega al contexto:
        - Presentaciones activas
        - Imágenes para galería
        - Imágenes para descripción
        - Videos del producto
        - Especificaciones técnicas
        - Productos relacionados
        """
        context = super().get_context_data(**kwargs)
        
        # Presentaciones activas del producto
        context['presentaciones'] = self.object.presentaciones.filter(activo=True)
        
        # Imágenes para la galería (parte superior)
        context['imagenes_galeria'] = self.object.imagenes_galeria
        
        # Imágenes para la descripción (pestaña descripción)
        context['imagenes_descripcion'] = self.object.imagenes_descripcion
        
        # Videos del producto
        context['videos'] = self.object.videos.all().order_by('orden')
        
        # Especificaciones técnicas
        context['especificaciones'] = self.object.especificaciones.all().order_by('orden')
        
        # Productos relacionados (misma categoría)
        context['productos_relacionados'] = Producto.objects.filter(
            categoria=self.object.categoria,
            activo=True,
            presentaciones__activo=True
        ).exclude(pk=self.object.pk).distinct()[:4]
        
        return context


def inicio(request):
    """
    Vista de la página de inicio.
    
    Muestra productos destacados y categorías principales.
    """
    # Productos destacados
    productos_destacados = Producto.objects.filter(
        activo=True,
        destacado=True,
        presentaciones__activo=True
    ).distinct().select_related('categoria', 'marca').prefetch_related('presentaciones')[:8]
    
    # Categorías principales (solo las que no tienen padre)
    categorias = Categoria.objects.filter(
        activo=True,
        categoria_padre__isnull=True
    ).prefetch_related('subcategorias')[:6]
    
    # Productos recientes
    productos_recientes = Producto.objects.filter(
        activo=True,
        presentaciones__activo=True
    ).distinct().select_related('categoria', 'marca').prefetch_related('presentaciones').order_by('-fecha_creacion')[:8]
    
    context = {
        'productos_destacados': productos_destacados,
        'categorias': categorias,
        'productos_recientes': productos_recientes,
    }
    
    return render(request, 'catalogo/inicio.html', context)
