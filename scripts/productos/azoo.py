"""
Productos de las marcas Azoo y Azoo Plus - Fertilizantes y Sustratos.
"""
from base import obtener_marca, obtener_categoria, crear_producto

def agregar_productos_azoo():
    """Agrega productos Azoo."""
    marca = obtener_marca('Azoo')
    if not marca:
        return
    
    # Fertilizantes
    cat = obtener_categoria('Fertilizantes')
    if cat:
        crear_producto(
            nombre='Azoo Carbon Plus',
            categoria=cat, marca=marca,
            descripcion='<p>Fuente de carbono líquido para plantas acuáticas.</p><ul><li>Alternativa al CO2</li><li>Fácil dosificación</li><li>Resultados rápidos</li></ul>',
            presentaciones=[
                {'nombre': '120ml', 'precio': 12.90},
                {'nombre': '250ml', 'precio': 22.90},
                {'nombre': '500ml', 'precio': 38.90},
            ]
        )
        crear_producto(
            nombre='Azoo Plant Grower',
            categoria=cat, marca=marca,
            descripcion='<p>Fertilizante completo para plantas acuáticas.</p><ul><li>Macro y micronutrientes</li><li>Promueve crecimiento vigoroso</li><li>No promueve algas</li></ul>',
            presentaciones=[
                {'nombre': '120ml', 'precio': 11.90},
                {'nombre': '250ml', 'precio': 21.90},
                {'nombre': '500ml', 'precio': 36.90},
            ]
        )
        crear_producto(
            nombre='Azoo Iron Plus',
            categoria=cat, marca=marca,
            descripcion='<p>Hierro concentrado para plantas rojas.</p><ul><li>Hierro quelado</li><li>Intensifica colores rojos</li><li>Fácil absorción</li></ul>',
            presentaciones=[
                {'nombre': '120ml', 'precio': 10.90},
                {'nombre': '250ml', 'precio': 19.90},
            ]
        )

def agregar_productos_azoo_plus():
    """Agrega productos Azoo Plus."""
    marca = obtener_marca('Azoo Plus')
    if not marca:
        return
    
    # Sustratos
    cat = obtener_categoria('Sustratos')
    if cat:
        crear_producto(
            nombre='Azoo Plant Grower Bed',
            categoria=cat, marca=marca,
            descripcion='<p>Sustrato nutritivo profesional para plantas.</p><ul><li>Rico en nutrientes</li><li>pH neutro</li><li>No enturbia el agua</li></ul>',
            presentaciones=[
                {'nombre': '3L', 'precio': 29.90},
                {'nombre': '9L', 'precio': 69.90},
            ]
        )
        crear_producto(
            nombre='Azoo Black Earth Soil',
            categoria=cat, marca=marca,
            descripcion='<p>Sustrato activo negro para acuarios plantados.</p><ul><li>Reduce pH y dureza</li><li>Ideal para plantas exigentes</li><li>Color negro intenso</li></ul>',
            presentaciones=[
                {'nombre': '3L', 'precio': 32.90},
                {'nombre': '9L', 'precio': 79.90},
            ]
        )

if __name__ == '__main__':
    print("🌱 Agregando productos Azoo...")
    agregar_productos_azoo()
    print("🌱 Agregando productos Azoo Plus...")
    agregar_productos_azoo_plus()
    print("✨ Completado!")
