"""
Productos de la marca Week Aqua - Lámparas.
"""
from base import obtener_marca, obtener_categoria, crear_producto

def agregar_productos_week_aqua():
    """Agrega productos Week Aqua."""
    marca = obtener_marca('Week Aqua')
    if not marca:
        return
    
    # Altos Requerimientos (Lámparas)
    cat = obtener_categoria('Altos Requerimientos')
    if cat:
        crear_producto(
            nombre='Week Aqua M Series Pro',
            categoria=cat, marca=marca,
            descripcion='<p>Lámpara LED profesional de alto rendimiento.</p><ul><li>LEDs WRGB de última generación</li><li>Control por app</li><li>Diseño ultra delgado</li></ul>',
            presentaciones=[
                {'nombre': 'M300 Pro (30cm)', 'precio': 119.90},
                {'nombre': 'M450 Pro (45cm)', 'precio': 149.90},
                {'nombre': 'M600 Pro (60cm)', 'precio': 189.90},
                {'nombre': 'M900 Pro (90cm)', 'precio': 259.90},
            ]
        )
        crear_producto(
            nombre='Week Aqua K Series',
            categoria=cat, marca=marca,
            descripcion='<p>Lámpara LED potente para acuarios plantados.</p><ul><li>Espectro completo</li><li>Cuerpo de aluminio</li><li>Alta PAR</li></ul>',
            presentaciones=[
                {'nombre': 'K300 (30cm)', 'precio': 89.90},
                {'nombre': 'K450 (45cm)', 'precio': 109.90},
                {'nombre': 'K600 (60cm)', 'precio': 139.90},
            ]
        )

if __name__ == '__main__':
    print("💡 Agregando productos Week Aqua...")
    agregar_productos_week_aqua()
    print("✨ Completado!")
