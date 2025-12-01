"""
Vistas para la gestión de pedidos.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction

from apps.carrito.carrito import Carrito
from .models import Pedido, ItemPedido
from .forms import CheckoutForm
from .emails import enviar_confirmacion_pedido, enviar_notificacion_admin, generar_link_whatsapp


def checkout(request):
    """
    Vista del proceso de checkout.
    
    Muestra el formulario de datos del cliente y procesa el pedido.
    """
    carrito = Carrito(request)
    
    # Verificar que el carrito no esté vacío
    if len(carrito) == 0:
        messages.warning(request, 'Tu carrito está vacío')
        return redirect('catalogo:producto_lista')
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Crear el pedido
                    pedido = Pedido.objects.create(
                        nombre=form.cleaned_data['nombre'],
                        email=form.cleaned_data['email'],
                        telefono=form.cleaned_data.get('telefono', ''),
                        direccion=form.cleaned_data['direccion'],
                        ciudad=form.cleaned_data['ciudad'],
                        codigo_postal=form.cleaned_data['codigo_postal'],
                        notas=form.cleaned_data.get('notas', ''),
                    )
                    
                    # Crear los items del pedido
                    for item in carrito:
                        presentacion = item['presentacion']
                        
                        # Verificar stock
                        if item['cantidad'] > presentacion.stock:
                            raise ValueError(
                                f'Stock insuficiente para {presentacion.producto.nombre} - {presentacion.nombre}'
                            )
                        
                        # Crear item
                        ItemPedido.objects.create(
                            pedido=pedido,
                            presentacion=presentacion,
                            producto_nombre=presentacion.producto.nombre,
                            presentacion_nombre=presentacion.nombre,
                            precio=item['precio'],
                            cantidad=item['cantidad'],
                        )
                        
                        # Actualizar stock
                        presentacion.stock -= item['cantidad']
                        presentacion.save()
                    
                    # Calcular total
                    pedido.calcular_total()
                    
                    # Limpiar carrito
                    carrito.limpiar()
                    
                    # Enviar emails
                    enviar_confirmacion_pedido(pedido)  # Al cliente
                    enviar_notificacion_admin(pedido)   # Al admin
                    
                    messages.success(request, f'¡Pedido {pedido.numero_pedido} creado exitosamente!')
                    return redirect('pedidos:confirmacion', numero_pedido=pedido.numero_pedido)
                    
            except ValueError as e:
                messages.error(request, str(e))
            except Exception as e:
                messages.error(request, 'Error al procesar el pedido. Intenta nuevamente.')
    else:
        form = CheckoutForm()
    
    return render(request, 'pedidos/checkout.html', {
        'form': form,
        'carrito': carrito,
    })


def confirmacion(request, numero_pedido):
    """
    Muestra la confirmación del pedido con datos bancarios y botón de WhatsApp.
    """
    pedido = get_object_or_404(Pedido, numero_pedido=numero_pedido)
    whatsapp_link = generar_link_whatsapp(pedido)
    
    return render(request, 'pedidos/confirmacion.html', {
        'pedido': pedido,
        'whatsapp_link': whatsapp_link,
    })


def consultar_pedido(request):
    """
    Permite consultar el estado de un pedido con email y número de pedido.
    """
    pedido = None
    error = None
    
    if request.method == 'POST':
        numero = request.POST.get('numero_pedido', '').strip().upper()
        email = request.POST.get('email', '').strip().lower()
        
        try:
            pedido = Pedido.objects.get(
                numero_pedido=numero,
                email__iexact=email
            )
        except Pedido.DoesNotExist:
            error = 'No se encontró ningún pedido con esos datos'
    
    return render(request, 'pedidos/consultar.html', {
        'pedido': pedido,
        'error': error,
    })

