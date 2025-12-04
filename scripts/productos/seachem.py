"""
Productos de la marca Seachem - Fertilizantes y Filtros.
"""
from base import obtener_marca, obtener_categoria, crear_producto

def agregar_productos_seachem():
    """Agrega productos Seachem."""
    marca = obtener_marca('Seachem')
    if not marca:
        return
    
    # Fertilizantes
    cat = obtener_categoria('Fertilizantes')
    if cat:
        crear_producto(
            nombre='Seachem Flourish',
            categoria=cat, marca=marca,
            descripcion='<p>Suplemento completo de micronutrientes para plantas acuáticas.</p><ul><li>Contiene hierro, manganeso, calcio</li><li>Vitaminas y aminoácidos</li><li>Uso semanal</li></ul>',
            presentaciones=[
                {'nombre': '100ml', 'precio': 12.90},
                {'nombre': '250ml', 'precio': 24.90},
                {'nombre': '500ml', 'precio': 42.90},
            ]
        )
        crear_producto(
            nombre='Seachem Flourish Excel',
            categoria=cat, marca=marca,
            descripcion='<p>Fuente de carbono orgánico biodisponible para plantas.</p><ul><li>Alternativa al CO2 inyectado</li><li>Mejora el crecimiento</li><li>Reduce algas</li></ul>',
            presentaciones=[
                {'nombre': '100ml', 'precio': 14.90},
                {'nombre': '250ml', 'precio': 28.90},
                {'nombre': '500ml', 'precio': 49.90},
            ]
        )
        crear_producto(
            nombre='Seachem Flourish Iron',
            categoria=cat, marca=marca,
            descripcion='<p>Hierro gluconato altamente disponible para plantas.</p><ul><li>Corrige deficiencias de hierro</li><li>Mejora coloración de plantas rojas</li><li>No precipita</li></ul>',
            presentaciones=[
                {'nombre': '100ml', 'precio': 11.90},
                {'nombre': '250ml', 'precio': 22.90},
            ]
        )
        crear_producto(
            nombre='Seachem Flourish Nitrogen',
            categoria=cat, marca=marca,
            descripcion='<p>Suplemento de nitrógeno en forma de nitrato y amonio.</p><ul><li>Para acuarios con pocos peces</li><li>Promueve crecimiento vigoroso</li><li>Fórmula balanceada</li></ul>',
            presentaciones=[
                {'nombre': '250ml', 'precio': 18.90},
                {'nombre': '500ml', 'precio': 32.90},
            ]
        )
        crear_producto(
            nombre='Seachem Flourish Phosphorus',
            categoria=cat, marca=marca,
            descripcion='<p>Fuente de fósforo para plantas de alta demanda.</p><ul><li>Corrige deficiencias</li><li>Mejora el crecimiento de raíces</li><li>Seguro para peces</li></ul>',
            presentaciones=[
                {'nombre': '250ml', 'precio': 18.90},
                {'nombre': '500ml', 'precio': 32.90},
            ]
        )
        crear_producto(
            nombre='Seachem Flourish Potassium',
            categoria=cat, marca=marca,
            descripcion='<p>Potasio esencial para plantas acuáticas.</p><ul><li>El macronutriente más deficiente</li><li>Previene hojas amarillas</li><li>No afecta pH</li></ul>',
            presentaciones=[
                {'nombre': '250ml', 'precio': 16.90},
                {'nombre': '500ml', 'precio': 29.90},
            ]
        )
        crear_producto(
            nombre='Seachem Flourish Trace',
            categoria=cat, marca=marca,
            descripcion='<p>Mezcla de oligoelementos esenciales para plantas.</p><ul><li>Complementa Flourish</li><li>Uso entre dosificaciones</li><li>Para acuarios plantados intensivos</li></ul>',
            presentaciones=[
                {'nombre': '100ml', 'precio': 12.90},
                {'nombre': '250ml', 'precio': 24.90},
            ]
        )
    
    # Sustratos
    cat = obtener_categoria('Sustratos')
    if cat:
        crear_producto(
            nombre='Seachem Flourite',
            categoria=cat, marca=marca,
            descripcion='<p>Sustrato poroso de arcite estable para plantas.</p><ul><li>No altera parámetros del agua</li><li>Duración permanente</li><li>Poroso para bacterias beneficiosas</li></ul>',
            presentaciones=[
                {'nombre': '3.5kg', 'precio': 34.90},
                {'nombre': '7kg', 'precio': 59.90},
            ]
        )
        crear_producto(
            nombre='Seachem Flourite Black',
            categoria=cat, marca=marca,
            descripcion='<p>Versión negra del sustrato Flourite, más estético.</p><ul><li>Color negro natural</li><li>Realza colores de peces y plantas</li><li>Estable y duradero</li></ul>',
            presentaciones=[
                {'nombre': '3.5kg', 'precio': 36.90},
                {'nombre': '7kg', 'precio': 64.90},
            ]
        )
        crear_producto(
            nombre='Seachem Onyx Sand',
            categoria=cat, marca=marca,
            descripcion='<p>Arena negra que aporta minerales a las plantas.</p><ul><li>Rico en calcio y magnesio</li><li>Ideal para plantas de raíz</li><li>Grano fino</li></ul>',
            presentaciones=[
                {'nombre': '3.5kg', 'precio': 32.90},
                {'nombre': '7kg', 'precio': 56.90},
            ]
        )

if __name__ == '__main__':
    print("🧪 Agregando productos Seachem...")
    agregar_productos_seachem()
    print("✨ Completado!")
