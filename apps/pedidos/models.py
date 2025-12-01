"""
Modelos para la gestión de pedidos.

Permite procesar pedidos sin necesidad de registro de usuario.
Solo se requieren datos de contacto y envío.
"""
import uuid
from django.db import models
from django.core.validators import RegexValidator

from apps.catalogo.models import Presentacion


class Pedido(models.Model):
    """
    Modelo para los pedidos de la tienda.
    
    Almacena la información del cliente y el estado del pedido.
    No requiere cuenta de usuario - solo datos de contacto.
    
    Atributos:
        numero_pedido (str): Número único del pedido.
        nombre (str): Nombre completo del cliente.
        email (str): Correo electrónico para notificaciones.
        telefono (str): Teléfono de contacto (opcional).
        direccion (str): Dirección de envío.
        ciudad (str): Ciudad de envío.
        codigo_postal (str): Código postal.
        notas (str): Notas adicionales del cliente.
        estado (str): Estado actual del pedido.
        total (Decimal): Total del pedido.
        creado (datetime): Fecha de creación.
        actualizado (datetime): Fecha de última actualización.
    """
    
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('confirmado', 'Confirmado'),
        ('en_proceso', 'En Proceso'),
        ('enviado', 'Enviado'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    ]
    
    # Validador para teléfono
    telefono_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="El teléfono debe tener entre 9 y 15 dígitos."
    )
    
    numero_pedido = models.CharField(
        max_length=32,
        unique=True,
        editable=False,
        verbose_name='Número de Pedido'
    )
    
    # Datos del cliente
    nombre = models.CharField(
        max_length=200,
        verbose_name='Nombre completo'
    )
    email = models.EmailField(
        verbose_name='Correo electrónico',
        help_text='Para enviar confirmación y actualizaciones del pedido'
    )
    telefono = models.CharField(
        max_length=17,
        blank=True,
        validators=[telefono_regex],
        verbose_name='Teléfono',
        help_text='Para contacto rápido (opcional)'
    )
    
    # Datos de envío
    direccion = models.TextField(
        verbose_name='Dirección de envío'
    )
    ciudad = models.CharField(
        max_length=100,
        verbose_name='Ciudad'
    )
    codigo_postal = models.CharField(
        max_length=10,
        verbose_name='Código Postal'
    )
    
    # Información adicional
    notas = models.TextField(
        blank=True,
        verbose_name='Notas adicionales',
        help_text='Instrucciones especiales de entrega'
    )
    
    # Estado y totales
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='pendiente',
        verbose_name='Estado'
    )
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name='Total'
    )
    
    # Fechas
    creado = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación'
    )
    actualizado = models.DateTimeField(
        auto_now=True,
        verbose_name='Última actualización'
    )
    
    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['-creado']
    
    def __str__(self):
        """Retorna el número de pedido."""
        return f"Pedido {self.numero_pedido}"
    
    def save(self, *args, **kwargs):
        """
        Genera el número de pedido automáticamente antes de guardar.
        """
        if not self.numero_pedido:
            self.numero_pedido = self._generar_numero_pedido()
        super().save(*args, **kwargs)
    
    def _generar_numero_pedido(self):
        """
        Genera un número de pedido único.
        
        Formato: GA-XXXXXXXX (8 caracteres hexágonales)
        """
        return f"GA-{uuid.uuid4().hex[:8].upper()}"
    
    @property
    def cantidad_items(self):
        """Retorna la cantidad total de items en el pedido."""
        return sum(item.cantidad for item in self.items.all())
    
    def calcular_total(self):
        """Calcula y guarda el total del pedido."""
        self.total = sum(item.subtotal for item in self.items.all())
        self.save(update_fields=['total'])


class ItemPedido(models.Model):
    """
    Modelo para los items individuales de un pedido.
    
    Guarda una copia de los datos del producto al momento de la compra
    para mantener un historial preciso.
    
    Atributos:
        pedido (ForeignKey): Pedido al que pertenece.
        presentacion (ForeignKey): Presentación comprada.
        producto_nombre (str): Nombre del producto (copia).
        presentacion_nombre (str): Nombre de la presentación (copia).
        precio (Decimal): Precio al momento de la compra.
        cantidad (int): Cantidad comprada.
    """
    
    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Pedido'
    )
    presentacion = models.ForeignKey(
        Presentacion,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Presentación'
    )
    
    # Copias de datos (para historial)
    producto_nombre = models.CharField(
        max_length=300,
        verbose_name='Producto'
    )
    presentacion_nombre = models.CharField(
        max_length=100,
        verbose_name='Presentación'
    )
    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Precio unitario'
    )
    cantidad = models.PositiveIntegerField(
        default=1,
        verbose_name='Cantidad'
    )
    
    class Meta:
        verbose_name = 'Item de Pedido'
        verbose_name_plural = 'Items de Pedido'
    
    def __str__(self):
        """Retorna descripción del item."""
        return f"{self.cantidad}x {self.producto_nombre} - {self.presentacion_nombre}"
    
    @property
    def subtotal(self):
        """Calcula el subtotal del item."""
        return self.precio * self.cantidad
