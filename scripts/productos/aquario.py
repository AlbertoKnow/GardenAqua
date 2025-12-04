"""
Productos de la marca Aquario - Sustratos y Fertilizantes.
"""
from base import obtener_marca, obtener_categoria, crear_producto

def agregar_productos_aquario():
    """Agrega productos Aquario."""
    marca = obtener_marca('Aquario')
    if not marca:
        return
    
    # Sustratos
    cat = obtener_categoria('Sustratos')
    if cat:
        crear_producto(
            nombre='Aquario Neo Soil Plantas',
            categoria=cat, marca=marca,
            descripcion='<p>Sustrato activo premium para acuarios plantados.</p><ul><li>Reduce pH y KH</li><li>Rico en nutrientes</li><li>Gránulos uniformes</li></ul>',
            presentaciones=[
                {'nombre': '3L', 'precio': 34.90},
                {'nombre': '8L', 'precio': 74.90},
            ]
        )
        crear_producto(
            nombre='Aquario Neo Soil Camarones',
            categoria=cat, marca=marca,
            descripcion='<p>Sustrato diseñado para acuarios de gambas.</p><ul><li>Parámetros ideales para gambas</li><li>Estabiliza pH</li><li>Color marrón natural</li></ul>',
            presentaciones=[
                {'nombre': '3L', 'precio': 36.90},
                {'nombre': '8L', 'precio': 79.90},
            ]
        )
    
    # Fertilizantes
    cat = obtener_categoria('Fertilizantes')
    if cat:
        crear_producto(
            nombre='Aquario Neo Solution 1',
            categoria=cat, marca=marca,
            descripcion='<p>Fertilizante líquido completo para plantas.</p><ul><li>Fórmula todo en uno</li><li>Micro y macronutrientes</li><li>Para uso diario o semanal</li></ul>',
            presentaciones=[
                {'nombre': '300ml', 'precio': 18.90},
                {'nombre': '1L', 'precio': 49.90},
            ]
        )

if __name__ == '__main__':
    print("🌿 Agregando productos Aquario...")
    agregar_productos_aquario()
    print("✨ Completado!")
