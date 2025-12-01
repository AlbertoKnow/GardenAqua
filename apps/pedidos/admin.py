"""
Configuración del admin para la app pedidos.
"""
from django.contrib import admin
from django.contrib import messages
from .models import Pedido, ItemPedido
from .emails import enviar_actualizacion_estado


class ItemPedidoInline(admin.TabularInline):
    """
    Inline para mostrar los items dentro del pedido.
    """
    model = ItemPedido
    extra = 0
    readonly_fields = ['presentacion', 'producto_nombre', 'presentacion_nombre', 'precio', 'cantidad', 'get_subtotal']
    can_delete = False
    
    def get_subtotal(self, obj):
        """Muestra el subtotal del item."""
        return f"${obj.subtotal}"
    get_subtotal.short_description = 'Subtotal'
    
    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    """
    Configuración del admin para Pedido.
    
    Al cambiar el estado del pedido, se envía automáticamente
    un email de notificación al cliente.
    """
    list_display = [
        'numero_pedido', 
        'nombre', 
        'email', 
        'estado', 
        'total', 
        'cantidad_items',
        'creado'
    ]
    list_filter = ['estado', 'creado', 'ciudad']
    search_fields = ['numero_pedido', 'nombre', 'email', 'telefono']
    readonly_fields = ['numero_pedido', 'creado', 'actualizado', 'total']
    ordering = ['-creado']
    date_hierarchy = 'creado'
    
    fieldsets = (
        ('Información del Pedido', {
            'fields': ('numero_pedido', 'estado', 'total')
        }),
        ('Datos del Cliente', {
            'fields': ('nombre', 'email', 'telefono')
        }),
        ('Datos de Envío', {
            'fields': ('direccion', 'ciudad', 'codigo_postal')
        }),
        ('Información Adicional', {
            'fields': ('notas',),
            'classes': ('collapse',)
        }),
        ('Fechas', {
            'fields': ('creado', 'actualizado'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [ItemPedidoInline]
    
    def cantidad_items(self, obj):
        """Muestra la cantidad de items en el pedido."""
        return obj.cantidad_items
    cantidad_items.short_description = 'Items'
    
    def save_model(self, request, obj, form, change):
        """
        Sobrescribe el método save_model para enviar email
        cuando el estado del pedido cambia.
        
        Args:
            request: Objeto HttpRequest.
            obj: Instancia del modelo Pedido.
            form: Formulario del admin.
            change: True si es una edición, False si es creación.
        """
        if change and 'estado' in form.changed_data:
            # Obtener el estado anterior desde la base de datos
            estado_anterior = Pedido.objects.get(pk=obj.pk).estado
            
            # Guardar el modelo
            super().save_model(request, obj, form, change)
            
            # Enviar notificación con el estado anterior
            try:
                enviar_actualizacion_estado(obj, estado_anterior)
                messages.success(
                    request, 
                    f'Se ha enviado un email de notificación a {obj.email}'
                )
            except Exception as e:
                messages.warning(
                    request, 
                    f'El pedido se guardó pero hubo un error al enviar el email: {e}'
                )
        else:
            super().save_model(request, obj, form, change)


@admin.register(ItemPedido)
class ItemPedidoAdmin(admin.ModelAdmin):
    """
    Configuración del admin para ItemPedido.
    """
    list_display = ['pedido', 'producto_nombre', 'presentacion_nombre', 'precio', 'cantidad', 'get_subtotal']
    list_filter = ['pedido__estado']
    search_fields = ['pedido__numero_pedido', 'producto_nombre']
    readonly_fields = ['pedido', 'presentacion', 'producto_nombre', 'presentacion_nombre', 'precio', 'cantidad']
    
    def get_subtotal(self, obj):
        """Muestra el subtotal del item."""
        return f"${obj.subtotal}"
    get_subtotal.short_description = 'Subtotal'
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
