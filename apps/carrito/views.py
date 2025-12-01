"""
Vistas para el carrito de compras.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.contrib import messages

from apps.catalogo.models import Presentacion
from .carrito import Carrito


def carrito_detalle(request):
    """
    Muestra el contenido del carrito de compras.
    """
    carrito = Carrito(request)
    
    return render(request, 'carrito/detalle.html', {
        'carrito': carrito,
    })


@require_POST
def carrito_agregar(request, presentacion_id):
    """
    Agrega una presentación al carrito.
    
    Args:
        presentacion_id: ID de la presentación a agregar.
    """
    carrito = Carrito(request)
    presentacion = get_object_or_404(Presentacion, id=presentacion_id, activo=True)
    
    cantidad = int(request.POST.get('cantidad', 1))
    
    # Verificar stock disponible
    cantidad_actual = carrito.carrito.get(str(presentacion_id), {}).get('cantidad', 0)
    cantidad_total = cantidad_actual + cantidad
    
    if cantidad_total > presentacion.stock:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'message': f'Stock insuficiente. Disponibles: {presentacion.stock}'
            })
        messages.error(request, f'Stock insuficiente. Disponibles: {presentacion.stock}')
        return redirect(request.META.get('HTTP_REFERER', 'carrito:detalle'))
    
    carrito.agregar(presentacion, cantidad)
    
    # Respuesta AJAX
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': f'{presentacion.producto.nombre} - {presentacion.nombre} agregado al carrito',
            'cantidad_carrito': len(carrito),
            'total_carrito': str(carrito.total),
        })
    
    messages.success(request, f'{presentacion.producto.nombre} - {presentacion.nombre} agregado al carrito')
    return redirect('carrito:detalle')


@require_POST
def carrito_eliminar(request, presentacion_id):
    """
    Elimina una presentación del carrito.
    """
    carrito = Carrito(request)
    presentacion = get_object_or_404(Presentacion, id=presentacion_id)
    
    carrito.eliminar(presentacion)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': 'Producto eliminado del carrito',
            'cantidad_carrito': len(carrito),
            'total_carrito': str(carrito.total),
        })
    
    messages.success(request, 'Producto eliminado del carrito')
    return redirect('carrito:detalle')


@require_POST
def carrito_actualizar(request, presentacion_id):
    """
    Actualiza la cantidad de una presentación en el carrito.
    """
    carrito = Carrito(request)
    presentacion = get_object_or_404(Presentacion, id=presentacion_id)
    
    cantidad = int(request.POST.get('cantidad', 1))
    
    # Verificar stock
    if cantidad > presentacion.stock:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'message': f'Stock insuficiente. Disponibles: {presentacion.stock}'
            })
        messages.error(request, f'Stock insuficiente. Disponibles: {presentacion.stock}')
        return redirect('carrito:detalle')
    
    carrito.actualizar_cantidad(presentacion, cantidad)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Calcular subtotal del item
        subtotal = presentacion.precio_actual * cantidad
        return JsonResponse({
            'success': True,
            'cantidad_carrito': len(carrito),
            'total_carrito': str(carrito.total),
            'subtotal_item': str(subtotal),
        })
    
    return redirect('carrito:detalle')


def carrito_limpiar(request):
    """
    Vacía completamente el carrito.
    """
    carrito = Carrito(request)
    carrito.limpiar()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': 'Carrito vaciado',
        })
    
    messages.success(request, 'Carrito vaciado')
    return redirect('carrito:detalle')
