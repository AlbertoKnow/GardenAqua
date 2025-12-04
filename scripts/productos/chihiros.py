"""
Productos de la marca Chihiros - Lámparas.
"""
from base import obtener_marca, obtener_categoria, crear_producto

def agregar_productos_chihiros():
    """Agrega productos Chihiros."""
    marca = obtener_marca('Chihiros')
    if not marca:
        return
    
    # Altos Requerimientos (Lámparas)
    cat = obtener_categoria('Altos Requerimientos')
    if cat:
        crear_producto(
            nombre='Chihiros WRGB II Slim',
            categoria=cat, marca=marca,
            descripcion='<p>Lámpara LED RGB profesional de perfil delgado.</p><ul><li>Control vía app Bluetooth</li><li>Espectro RGB completo</li><li>Simulación amanecer/atardecer</li></ul>',
            presentaciones=[
                {'nombre': '30cm', 'precio': 129.90},
                {'nombre': '45cm', 'precio': 159.90},
                {'nombre': '60cm', 'precio': 199.90},
                {'nombre': '90cm', 'precio': 279.90},
            ]
        )
        crear_producto(
            nombre='Chihiros Vivid 2',
            categoria=cat, marca=marca,
            descripcion='<p>Lámpara RGB de última generación para acuascaping profesional.</p><ul><li>LEDs de alta eficiencia</li><li>Colores vibrantes</li><li>Control inteligente</li></ul>',
            presentaciones=[
                {'nombre': '30cm', 'precio': 149.90},
                {'nombre': '45cm', 'precio': 189.90},
                {'nombre': '60cm', 'precio': 229.90},
            ]
        )
        crear_producto(
            nombre='Chihiros A II Series',
            categoria=cat, marca=marca,
            descripcion='<p>Lámpara LED de alta potencia para plantas exigentes.</p><ul><li>Aluminio para disipación</li><li>Compatible con Bluetooth</li><li>Alta eficiencia lumínica</li></ul>',
            presentaciones=[
                {'nombre': 'A II 301 (30cm)', 'precio': 69.90},
                {'nombre': 'A II 401 (40cm)', 'precio': 84.90},
                {'nombre': 'A II 601 (60cm)', 'precio': 109.90},
                {'nombre': 'A II 901 (90cm)', 'precio': 149.90},
            ]
        )
        crear_producto(
            nombre='Chihiros CII Series',
            categoria=cat, marca=marca,
            descripcion='<p>Lámpara LED económica ideal para principiantes.</p><ul><li>Buena relación calidad-precio</li><li>Para plantas de demanda media</li><li>Bajo consumo</li></ul>',
            presentaciones=[
                {'nombre': 'CII 251 (25cm)', 'precio': 34.90},
                {'nombre': 'CII 361 (36cm)', 'precio': 44.90},
                {'nombre': 'CII 451 (45cm)', 'precio': 54.90},
                {'nombre': 'CII 601 (60cm)', 'precio': 69.90},
            ]
        )

if __name__ == '__main__':
    print("💡 Agregando productos Chihiros...")
    agregar_productos_chihiros()
    print("✨ Completado!")
