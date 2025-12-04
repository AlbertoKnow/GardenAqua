"""
Productos de la marca Tropical - Alimentos.
"""
from base import obtener_marca, obtener_categoria, crear_producto

def agregar_productos_tropical():
    """Agrega productos Tropical."""
    marca = obtener_marca('Tropical')
    if not marca:
        return
    
    # Granulado
    cat = obtener_categoria('Granulado')
    if cat:
        crear_producto(
            nombre='Tropical Micro Granulat',
            categoria=cat, marca=marca,
            descripcion='<p>Alimento granulado de alta calidad para peces pequeños de agua dulce.</p><ul><li>Gránulos finos que se hunden lentamente</li><li>Enriquecido con vitaminas</li><li>Favorece la coloración natural</li></ul>',
            presentaciones=[
                {'nombre': '50g', 'precio': 8.50},
                {'nombre': '100g', 'precio': 14.90},
                {'nombre': '250g', 'precio': 29.90},
            ]
        )
        crear_producto(
            nombre='Tropical Cichlid Gran',
            categoria=cat, marca=marca,
            descripcion='<p>Alimento premium en gránulos para cíclidos africanos y americanos.</p><ul><li>Alto contenido proteico</li><li>Intensifica los colores</li><li>Gránulos que flotan y se hunden</li></ul>',
            presentaciones=[
                {'nombre': '100g', 'precio': 12.90},
                {'nombre': '250g', 'precio': 24.90},
                {'nombre': '500g', 'precio': 42.90},
            ]
        )
        crear_producto(
            nombre='Tropical Red Mico Colour Sticks',
            categoria=cat, marca=marca,
            descripcion='<p>Gránulos flotantes que intensifican el color rojo de los peces.</p><ul><li>Con astaxantina natural</li><li>Para peces tropicales</li><li>Fácil digestión</li></ul>',
            presentaciones=[
                {'nombre': '100g', 'precio': 11.90},
                {'nombre': '250g', 'precio': 22.90},
            ]
        )
    
    # Pellets
    cat = obtener_categoria('Pellets')
    if cat:
        crear_producto(
            nombre='Tropical Cichlid Pellets',
            categoria=cat, marca=marca,
            descripcion='<p>Pellets nutritivos para cíclidos de todos los tamaños.</p><ul><li>Fórmula balanceada</li><li>Mejora el sistema inmune</li><li>No enturbia el agua</li></ul>',
            presentaciones=[
                {'nombre': '100g', 'precio': 10.90},
                {'nombre': '250g', 'precio': 21.90},
                {'nombre': '500g', 'precio': 38.90},
            ]
        )
        crear_producto(
            nombre='Tropical Betta Pellet',
            categoria=cat, marca=marca,
            descripcion='<p>Pellets pequeños especialmente formulados para Bettas.</p><ul><li>Potencia colores rojos y azules</li><li>Alto contenido proteico</li><li>Tamaño ideal para Bettas</li></ul>',
            presentaciones=[
                {'nombre': '10g', 'precio': 5.50},
                {'nombre': '30g', 'precio': 12.90},
            ]
        )
    
    # Pastillas
    cat = obtener_categoria('Pastillas')
    if cat:
        crear_producto(
            nombre='Tropical Pleco Tablets',
            categoria=cat, marca=marca,
            descripcion='<p>Pastillas vegetales para plecos y peces de fondo.</p><ul><li>36% de espirulina</li><li>Se hunden rápidamente</li><li>Rico en fibra vegetal</li></ul>',
            presentaciones=[
                {'nombre': '50g', 'precio': 9.90},
                {'nombre': '125g', 'precio': 19.90},
                {'nombre': '250g', 'precio': 34.90},
            ]
        )
        crear_producto(
            nombre='Tropical Catfish Tablets',
            categoria=cat, marca=marca,
            descripcion='<p>Pastillas nutritivas para bagres y corydoras.</p><ul><li>Alto valor proteico</li><li>Libera nutrientes gradualmente</li><li>Ideal para alimentación nocturna</li></ul>',
            presentaciones=[
                {'nombre': '50g', 'precio': 8.90},
                {'nombre': '125g', 'precio': 17.90},
            ]
        )
    
    # Sticks
    cat = obtener_categoria('Sticks')
    if cat:
        crear_producto(
            nombre='Tropical Goldfish Colour Sticks',
            categoria=cat, marca=marca,
            descripcion='<p>Sticks flotantes para goldfish que intensifican colores.</p><ul><li>Con carotenoides naturales</li><li>Fórmula flotante</li><li>Fácil digestión</li></ul>',
            presentaciones=[
                {'nombre': '100g', 'precio': 8.90},
                {'nombre': '250g', 'precio': 18.90},
                {'nombre': '500g', 'precio': 32.90},
            ]
        )
        crear_producto(
            nombre='Tropical Koi & Goldfish Sticks',
            categoria=cat, marca=marca,
            descripcion='<p>Sticks flotantes para kois y goldfish de estanque.</p><ul><li>Para alimentación en estanques</li><li>No contamina el agua</li><li>Favorece el crecimiento</li></ul>',
            presentaciones=[
                {'nombre': '250g', 'precio': 14.90},
                {'nombre': '500g', 'precio': 24.90},
                {'nombre': '1kg', 'precio': 42.90},
            ]
        )

    # Liofilizados
    cat = obtener_categoria('Liofilizados')
    if cat:
        crear_producto(
            nombre='Tropical FD Blood Worms',
            categoria=cat, marca=marca,
            descripcion='<p>Larvas de mosquito liofilizadas, golosina natural.</p><ul><li>100% natural</li><li>Alto contenido proteico</li><li>Estimula el apetito</li></ul>',
            presentaciones=[
                {'nombre': '10g', 'precio': 7.90},
                {'nombre': '25g', 'precio': 15.90},
            ]
        )
        crear_producto(
            nombre='Tropical FD Brine Shrimp',
            categoria=cat, marca=marca,
            descripcion='<p>Artemia liofilizada, alimento premium para peces tropicales.</p><ul><li>Rica en proteínas</li><li>Ideal como suplemento</li><li>Conserva nutrientes naturales</li></ul>',
            presentaciones=[
                {'nombre': '10g', 'precio': 8.90},
                {'nombre': '25g', 'precio': 17.90},
            ]
        )

if __name__ == '__main__':
    print("🐠 Agregando productos Tropical...")
    agregar_productos_tropical()
    print("✨ Completado!")
