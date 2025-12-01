"""
Funciones para envío de correos electrónicos usando Resend.

Este módulo maneja todos los emails transaccionales del sistema de pedidos:
- Confirmación de pedido al cliente
- Notificación de nuevo pedido al admin
- Actualización de estado del pedido

Documentación de Resend: https://resend.com/docs/send-with-python
"""
import urllib.parse
import resend
from django.conf import settings
from django.template.loader import render_to_string


# Configurar API Key de Resend
resend.api_key = settings.RESEND_API_KEY


def enviar_confirmacion_pedido(pedido):
    """
    Envía el correo de confirmación al cliente después de crear un pedido.
    
    Args:
        pedido: Instancia del modelo Pedido.
    
    Returns:
        dict | None: Respuesta de Resend si se envió, None si hubo error.
    """
    try:
        # Contexto para la plantilla
        context = {
            'pedido': pedido,
            'items': pedido.items.all(),
            'site_name': settings.SITE_NAME,
            'site_url': settings.SITE_URL,
            'whatsapp_number': settings.WHATSAPP_NUMBER,
            'whatsapp_link': generar_link_whatsapp(pedido),
        }
        
        # Renderizar plantilla HTML
        html_content = render_to_string('pedidos/emails/confirmacion.html', context)
        
        # Enviar email con Resend
        params = {
            "from": settings.RESEND_FROM_EMAIL,
            "to": [pedido.email],
            "reply_to": settings.RESEND_REPLY_TO,
            "subject": f"✅ Pedido {pedido.numero_pedido} - Confirmación",
            "html": html_content,
        }
        
        response = resend.Emails.send(params)
        print(f"✅ Email de confirmación enviado a {pedido.email}: {response}")
        return response
        
    except Exception as e:
        print(f"❌ Error al enviar email de confirmación: {e}")
        return None


def enviar_notificacion_admin(pedido):
    """
    Envía notificación al administrador cuando hay un nuevo pedido.
    
    Args:
        pedido: Instancia del modelo Pedido.
    
    Returns:
        dict | None: Respuesta de Resend si se envió, None si hubo error.
    """
    if not settings.ADMIN_EMAIL:
        print("⚠️ ADMIN_EMAIL no configurado, no se envía notificación")
        return None
        
    try:
        context = {
            'pedido': pedido,
            'items': pedido.items.all(),
            'site_name': settings.SITE_NAME,
            'site_url': settings.SITE_URL,
        }
        
        html_content = render_to_string('pedidos/emails/notificacion_admin.html', context)
        
        params = {
            "from": settings.RESEND_FROM_EMAIL,
            "to": [settings.ADMIN_EMAIL],
            "subject": f"🛒 Nuevo Pedido {pedido.numero_pedido} - S/{pedido.total}",
            "html": html_content,
        }
        
        response = resend.Emails.send(params)
        print(f"✅ Notificación enviada al admin: {response}")
        return response
        
    except Exception as e:
        print(f"❌ Error al enviar notificación al admin: {e}")
        return None


def enviar_actualizacion_estado(pedido, estado_anterior):
    """
    Envía un correo cuando el estado del pedido cambia.
    
    Args:
        pedido: Instancia del modelo Pedido.
        estado_anterior: Estado previo del pedido.
    
    Returns:
        dict | None: Respuesta de Resend si se envió, None si hubo error.
    """
    try:
        context = {
            'pedido': pedido,
            'estado_anterior': estado_anterior,
            'estado_anterior_display': dict(pedido.ESTADO_CHOICES).get(estado_anterior, estado_anterior),
            'site_name': settings.SITE_NAME,
            'site_url': settings.SITE_URL,
            'whatsapp_number': settings.WHATSAPP_NUMBER,
        }
        
        html_content = render_to_string('pedidos/emails/actualizacion_estado.html', context)
        
        # Emoji según el estado
        emojis = {
            'pendiente': '⏳',
            'pagado': '💳',
            'procesando': '📦',
            'enviado': '🚚',
            'entregado': '✅',
            'cancelado': '❌',
        }
        emoji = emojis.get(pedido.estado, '📋')
        
        params = {
            "from": settings.RESEND_FROM_EMAIL,
            "to": [pedido.email],
            "reply_to": settings.RESEND_REPLY_TO,
            "subject": f"{emoji} Tu pedido {pedido.numero_pedido} - {pedido.get_estado_display()}",
            "html": html_content,
        }
        
        response = resend.Emails.send(params)
        print(f"✅ Email de actualización enviado a {pedido.email}: {response}")
        return response
        
    except Exception as e:
        print(f"❌ Error al enviar email de actualización: {e}")
        return None


def generar_link_whatsapp(pedido):
    """
    Genera el link de WhatsApp con el mensaje del pedido prellenado.
    
    Args:
        pedido: Instancia del modelo Pedido.
    
    Returns:
        str: URL de WhatsApp con el mensaje codificado.
    """
    # Construir lista de productos
    items_texto = ""
    for item in pedido.items.all():
        items_texto += f"   - {item.producto_nombre}"
        if item.presentacion_nombre:
            items_texto += f" ({item.presentacion_nombre})"
        items_texto += f" x{item.cantidad} = S/{item.subtotal}\n"
    
    # Construir notas si existen
    notas_texto = f"\n*NOTAS:*\n{pedido.notas}" if pedido.notas else ""
    
    # Mensaje completo - formato limpio sin emojis
    mensaje = f"""================================
*PEDIDO GARDENAQUA*
================================

*N° Pedido:* {pedido.numero_pedido}

--------------------------------
*DATOS DEL CLIENTE*
--------------------------------
Nombre: {pedido.nombre}
Email: {pedido.email}
Telefono: {pedido.telefono or 'No proporcionado'}

--------------------------------
*PRODUCTOS*
--------------------------------
{items_texto}
*TOTAL: S/{pedido.total}*

--------------------------------
*DIRECCION DE ENVIO*
--------------------------------
{pedido.direccion}
{pedido.ciudad}{f', CP: {pedido.codigo_postal}' if pedido.codigo_postal else ''}
{notas_texto}
================================

_Adjuntare mi comprobante de pago a este mensaje._"""

    # Codificar mensaje para URL
    mensaje_codificado = urllib.parse.quote(mensaje, safe='')
    
    return f"https://wa.me/{settings.WHATSAPP_NUMBER}?text={mensaje_codificado}"
