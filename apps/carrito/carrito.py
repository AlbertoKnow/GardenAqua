"""
Clase Carrito para manejar el carrito de compras mediante sesiones.

Permite agregar, eliminar y modificar productos sin necesidad de registro.
"""
from decimal import Decimal
from apps.catalogo.models import Presentacion


class Carrito:
    """
    Clase que gestiona el carrito de compras usando sesiones de Django.
    
    Atributos:
        session: Sesión de Django donde se almacena el carrito.
        carrito: Diccionario con los items del carrito.
    """
    
    def __init__(self, request):
        """
        Inicializa el carrito desde la sesión del usuario.
        
        Args:
            request: Objeto HttpRequest de Django.
        """
        self.session = request.session
        carrito = self.session.get('carrito')
        
        if not carrito:
            # Crear carrito vacío en la sesión
            carrito = self.session['carrito'] = {}
        
        self.carrito = carrito
    
    def agregar(self, presentacion, cantidad=1):
        """
        Agrega una presentación al carrito o actualiza su cantidad.
        
        Args:
            presentacion: Instancia de Presentacion a agregar.
            cantidad: Cantidad a agregar (por defecto 1).
        """
        presentacion_id = str(presentacion.id)
        
        if presentacion_id not in self.carrito:
            self.carrito[presentacion_id] = {
                'cantidad': 0,
                'precio': str(presentacion.precio_actual),
            }
        
        self.carrito[presentacion_id]['cantidad'] += cantidad
        self.guardar()
    
    def eliminar(self, presentacion):
        """
        Elimina una presentación del carrito.
        
        Args:
            presentacion: Instancia de Presentacion a eliminar.
        """
        presentacion_id = str(presentacion.id)
        
        if presentacion_id in self.carrito:
            del self.carrito[presentacion_id]
            self.guardar()
    
    def actualizar_cantidad(self, presentacion, cantidad):
        """
        Actualiza la cantidad de una presentación en el carrito.
        
        Args:
            presentacion: Instancia de Presentacion.
            cantidad: Nueva cantidad.
        """
        presentacion_id = str(presentacion.id)
        
        if presentacion_id in self.carrito:
            if cantidad > 0:
                self.carrito[presentacion_id]['cantidad'] = cantidad
            else:
                self.eliminar(presentacion)
            self.guardar()
    
    def guardar(self):
        """Marca la sesión como modificada para guardar cambios."""
        self.session.modified = True
    
    def limpiar(self):
        """Vacía completamente el carrito."""
        del self.session['carrito']
        self.guardar()
    
    def __iter__(self):
        """
        Itera sobre los items del carrito con información completa.
        
        Yields:
            dict: Diccionario con datos del item (presentacion, cantidad, precio, subtotal).
        """
        presentacion_ids = self.carrito.keys()
        presentaciones = Presentacion.objects.filter(id__in=presentacion_ids).select_related(
            'producto', 'producto__categoria', 'producto__marca'
        )
        
        carrito = self.carrito.copy()
        
        for presentacion in presentaciones:
            carrito[str(presentacion.id)]['presentacion'] = presentacion
        
        for item in carrito.values():
            if 'presentacion' in item:
                item['precio'] = Decimal(item['precio'])
                item['subtotal'] = item['precio'] * item['cantidad']
                yield item
    
    def __len__(self):
        """Retorna el número total de items en el carrito."""
        return sum(item['cantidad'] for item in self.carrito.values())
    
    @property
    def total(self):
        """Calcula el total del carrito."""
        return sum(
            Decimal(item['precio']) * item['cantidad']
            for item in self.carrito.values()
        )
    
    @property
    def cantidad_items(self):
        """Retorna la cantidad de items únicos en el carrito."""
        return len(self.carrito)
