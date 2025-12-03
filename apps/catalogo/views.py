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
        Si la categoría es padre, incluye productos de todas sus subcategorías.
        Solo muestra productos activos con presentaciones activas.
        """
        queryset = Producto.objects.filter(
            activo=True,
            presentaciones__activo=True
        ).distinct().select_related('categoria', 'marca').prefetch_related('presentaciones')
        
        # Filtrar por categoría si se proporciona
        categoria_slug = self.kwargs.get('categoria_slug')
        if categoria_slug:
            categoria = get_object_or_404(Categoria, slug=categoria_slug, activo=True)
            
            # Obtener IDs de la categoría y todas sus subcategorías
            categorias_ids = [categoria.id]
            subcategorias = categoria.subcategorias.filter(activo=True)
            if subcategorias.exists():
                categorias_ids.extend(subcategorias.values_list('id', flat=True))
            
            queryset = queryset.filter(categoria_id__in=categorias_ids)
        
        # Filtrar por marca si se proporciona
        marca_slug = self.request.GET.get('marca')
        if marca_slug:
            queryset = queryset.filter(marca__slug=marca_slug)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        """Agrega las marcas y filtros actuales al contexto."""
        context = super().get_context_data(**kwargs)
        
        # Las categorías ya vienen del context_processor 'categorias'
        # Solo agregamos las marcas activas
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
    
    Muestra productos destacados, categorías principales y marcas.
    """
    # Productos destacados
    productos_destacados = Producto.objects.filter(
        activo=True,
        destacado=True,
        presentaciones__activo=True
    ).distinct().select_related('categoria', 'marca').prefetch_related('presentaciones')[:8]
    
    # Productos recientes
    productos_recientes = Producto.objects.filter(
        activo=True,
        presentaciones__activo=True
    ).distinct().select_related('categoria', 'marca').prefetch_related('presentaciones').order_by('-fecha_creacion')[:8]
    
    # Marcas activas con productos
    marcas = Marca.objects.filter(
        activo=True,
        productos__activo=True,
        productos__presentaciones__activo=True
    ).distinct().order_by('nombre')[:8]
    
    # Las categorías ya vienen del context_processor 'categorias'
    context = {
        'productos_destacados': productos_destacados,
        'productos_recientes': productos_recientes,
        'marcas': marcas,
    }
    
    return render(request, 'catalogo/inicio.html', context)
