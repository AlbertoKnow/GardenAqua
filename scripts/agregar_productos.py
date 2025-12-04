"""
Script para agregar productos de ejemplo a la tienda GardenAqua.

Este script crea productos variados para cada categoría y marca existente.
Las imágenes se agregarán manualmente después.
"""

import os
import sys
import django

# Configurar Django
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gardenaqua.settings')
django.setup()

from apps.catalogo.models import Marca, Categoria, Producto, Presentacion
from decimal import Decimal


def crear_productos():
    """
    Crea productos de ejemplo para la tienda.
    Solo crea productos que no existan (basándose en el nombre).
    """
    
    # Obtener marcas
    try:
        chihiros = Marca.objects.get(nombre='Chihiros')
        seachem = Seachem = Marca.objects.get(nombre='Seachem')
        tropical = Marca.objects.get(nombre='Tropical')
    except Marca.DoesNotExist as e:
        print(f"Error: No se encontró la marca - {e}")
        return
    
    # Obtener categorías
    try:
        alimentos = Categoria.objects.get(nombre='Alimentos')
        filtros = Categoria.objects.get(nombre='Filtros')
        lamparas = Categoria.objects.get(nombre='Lámparas')
    except Categoria.DoesNotExist as e:
        print(f"Error: No se encontró la categoría - {e}")
        return
    
    # Lista de productos a crear
    productos_data = [
        # === ALIMENTOS - Tropical ===
        {
            'nombre': 'Tropical Micro Granulat',
            'categoria': alimentos,
            'marca': tropical,
            'descripcion': '''<p>Alimento de alta calidad para peces pequeños y medianos de agua dulce.</p>
            <p><strong>Características:</strong></p>
            <ul>
                <li>Gránulos finos que se hunden lentamente</li>
                <li>Enriquecido con vitaminas y minerales esenciales</li>
                <li>Favorece la coloración natural de los peces</li>
                <li>Fácil digestión</li>
            </ul>''',
            'presentaciones': [
                {'nombre': '50g', 'precio': Decimal('8.50')},
                {'nombre': '100g', 'precio': Decimal('14.90')},
                {'nombre': '250g', 'precio': Decimal('29.90')},
            ]
        },
        {
            'nombre': 'Tropical Cichlid Gran',
            'categoria': alimentos,
            'marca': tropical,
            'descripcion': '''<p>Alimento premium en gránulos especialmente formulado para cíclidos.</p>
            <p><strong>Beneficios:</strong></p>
            <ul>
                <li>Alto contenido proteico para un crecimiento óptimo</li>
                <li>Intensifica los colores naturales</li>
                <li>Gránulos que flotan y se hunden gradualmente</li>
                <li>Ideal para cíclidos africanos y americanos</li>
            </ul>''',
            'presentaciones': [
                {'nombre': '100g', 'precio': Decimal('12.90')},
                {'nombre': '250g', 'precio': Decimal('24.90')},
                {'nombre': '500g', 'precio': Decimal('42.90')},
            ]
        },
        {
            'nombre': 'Tropical Spirulina Forte',
            'categoria': alimentos,
            'marca': tropical,
            'descripcion': '''<p>Alimento vegetal con alto contenido de espirulina para peces herbívoros.</p>
            <p><strong>Composición especial:</strong></p>
            <ul>
                <li>36% de espirulina natural</li>
                <li>Rico en vitaminas y antioxidantes</li>
                <li>Mejora el sistema inmunológico</li>
                <li>Perfecto para plecos, ancistrus y otros herbívoros</li>
            </ul>''',
            'presentaciones': [
                {'nombre': '50g', 'precio': Decimal('9.90')},
                {'nombre': '100g', 'precio': Decimal('16.90')},
                {'nombre': '250g', 'precio': Decimal('32.90')},
            ]
        },
        {
            'nombre': 'Tropical Betta Granulat',
            'categoria': alimentos,
            'marca': tropical,
            'descripcion': '''<p>Alimento especialmente formulado para peces Betta.</p>
            <p><strong>Características:</strong></p>
            <ul>
                <li>Gránulos pequeños ideales para la boca del Betta</li>
                <li>Potencia los colores rojos y azules</li>
                <li>Alto contenido proteico</li>
                <li>Fórmula que no enturbia el agua</li>
            </ul>''',
            'presentaciones': [
                {'nombre': '10g', 'precio': Decimal('5.50')},
                {'nombre': '30g', 'precio': Decimal('12.90')},
            ]
        },
        {
            'nombre': 'Tropical Goldfish Color',
            'categoria': alimentos,
            'marca': tropical,
            'descripcion': '''<p>Alimento completo para goldfish y carpas que intensifica su coloración.</p>
            <p><strong>Beneficios:</strong></p>
            <ul>
                <li>Enriquecido con carotenoides naturales</li>
                <li>Fórmula flotante</li>
                <li>Favorece el desarrollo saludable</li>
                <li>No contamina el agua</li>
            </ul>''',
            'presentaciones': [
                {'nombre': '100g', 'precio': Decimal('8.90')},
                {'nombre': '250g', 'precio': Decimal('18.90')},
                {'nombre': '500g', 'precio': Decimal('32.90')},
            ]
        },
        
        # === ALIMENTOS - Seachem ===
        {
            'nombre': 'Seachem NutriDiet Betta',
            'categoria': alimentos,
            'marca': seachem,
            'descripcion': '''<p>Alimento premium con probióticos para peces Betta.</p>
            <p><strong>Innovación Seachem:</strong></p>
            <ul>
                <li>Contiene GarlicGuard para estimular el apetito</li>
                <li>Probióticos para una digestión saludable</li>
                <li>Vitamina C estabilizada</li>
                <li>Mejora la respuesta inmune</li>
            </ul>''',
            'presentaciones': [
                {'nombre': '15g', 'precio': Decimal('11.90')},
                {'nombre': '30g', 'precio': Decimal('19.90')},
            ]
        },
        {
            'nombre': 'Seachem NutriDiet Cichlid Flakes',
            'categoria': alimentos,
            'marca': seachem,
            'descripcion': '''<p>Hojuelas nutritivas con probióticos para cíclidos.</p>
            <p><strong>Características premium:</strong></p>
            <ul>
                <li>Fórmula con Chlorella para colores vibrantes</li>
                <li>Probióticos que mejoran la digestión</li>
                <li>Rico en proteínas de alta calidad</li>
                <li>Ideal para cíclidos de todos los tamaños</li>
            </ul>''',
            'presentaciones': [
                {'nombre': '30g', 'precio': Decimal('14.90')},
                {'nombre': '100g', 'precio': Decimal('34.90')},
            ]
        },
        
        # === FILTROS - Seachem ===
        {
            'nombre': 'Seachem Matrix',
            'categoria': filtros,
            'marca': seachem,
            'descripcion': '''<p>Material filtrante biológico de alta capacidad.</p>
            <p><strong>Tecnología avanzada:</strong></p>
            <ul>
                <li>Estructura porosa interna y externa</li>
                <li>Permite colonización de bacterias anaeróbicas</li>
                <li>Reduce nitratos de forma natural</li>
                <li>Extremadamente duradero, nunca necesita reemplazo</li>
            </ul>''',
            'presentaciones': [
                {'nombre': '250ml', 'precio': Decimal('15.90')},
                {'nombre': '500ml', 'precio': Decimal('26.90')},
                {'nombre': '1L', 'precio': Decimal('44.90')},
                {'nombre': '2L', 'precio': Decimal('79.90')},
            ]
        },
        {
            'nombre': 'Seachem Purigen',
            'categoria': filtros,
            'marca': seachem,
            'descripcion': '''<p>Resina sintética premium para eliminación de impurezas.</p>
            <p><strong>Rendimiento superior:</strong></p>
            <ul>
                <li>Elimina compuestos nitrogenados orgánicos</li>
                <li>Cristaliza el agua del acuario</li>
                <li>Regenerable con lejía</li>
                <li>No afecta el pH ni la conductividad</li>
            </ul>''',
            'presentaciones': [
                {'nombre': '100ml', 'precio': Decimal('18.90')},
                {'nombre': '250ml', 'precio': Decimal('39.90')},
                {'nombre': '500ml', 'precio': Decimal('69.90')},
            ]
        },
        {
            'nombre': 'Seachem Pond Matrix',
            'categoria': filtros,
            'marca': seachem,
            'descripcion': '''<p>Medio filtrante biológico diseñado para estanques.</p>
            <p><strong>Para estanques:</strong></p>
            <ul>
                <li>Alta capacidad de carga biológica</li>
                <li>Soporta colonias bacterianas masivas</li>
                <li>Ideal para estanques de koi y goldfish</li>
                <li>Reduce mantenimiento del estanque</li>
            </ul>''',
            'presentaciones': [
                {'nombre': '2L', 'precio': Decimal('54.90')},
                {'nombre': '4L', 'precio': Decimal('89.90')},
            ]
        },
        {
            'nombre': 'Seachem De Nitrate',
            'categoria': filtros,
            'marca': seachem,
            'descripcion': '''<p>Medio filtrante poroso para eliminación de nitratos.</p>
            <p><strong>Beneficios:</strong></p>
            <ul>
                <li>Elimina nitratos, nitritos y amoníaco</li>
                <li>Porosidad óptima para bacterias desnitrificantes</li>
                <li>Puede usarse en agua dulce y salada</li>
                <li>Económico y efectivo</li>
            </ul>''',
            'presentaciones': [
                {'nombre': '250ml', 'precio': Decimal('12.90')},
                {'nombre': '500ml', 'precio': Decimal('21.90')},
                {'nombre': '1L', 'precio': Decimal('36.90')},
            ]
        },
        
        # === LÁMPARAS - Chihiros ===
        {
            'nombre': 'Chihiros A Series',
            'categoria': lamparas,
            'marca': chihiros,
            'descripcion': '''<p>Lámpara LED de alta eficiencia para acuarios plantados.</p>
            <p><strong>Especificaciones:</strong></p>
            <ul>
                <li>LEDs de alta potencia con espectro completo</li>
                <li>Cuerpo de aluminio para mejor disipación de calor</li>
                <li>Diseño delgado y elegante</li>
                <li>Compatible con controlador Bluetooth</li>
            </ul>''',
            'presentaciones': [
                {'nombre': 'A301 (30cm)', 'precio': Decimal('59.90')},
                {'nombre': 'A401 (40cm)', 'precio': Decimal('74.90')},
                {'nombre': 'A601 (60cm)', 'precio': Decimal('99.90')},
                {'nombre': 'A801 (80cm)', 'precio': Decimal('129.90')},
            ]
        },
        {
            'nombre': 'Chihiros C Series',
            'categoria': lamparas,
            'marca': chihiros,
            'descripcion': '''<p>Lámpara LED económica ideal para principiantes.</p>
            <p><strong>Características:</strong></p>
            <ul>
                <li>Relación calidad-precio excepcional</li>
                <li>Suficiente potencia para plantas de baja demanda</li>
                <li>Montaje flexible con soportes ajustables</li>
                <li>Bajo consumo energético</li>
            </ul>''',
            'presentaciones': [
                {'nombre': 'C251 (25cm)', 'precio': Decimal('29.90')},
                {'nombre': 'C361 (36cm)', 'precio': Decimal('39.90')},
                {'nombre': 'C451 (45cm)', 'precio': Decimal('49.90')},
                {'nombre': 'C561 (56cm)', 'precio': Decimal('59.90')},
            ]
        },
        {
            'nombre': 'Chihiros RGB Vivid 2',
            'categoria': lamparas,
            'marca': chihiros,
            'descripcion': '''<p>Lámpara LED RGB profesional para acuarios plantados de alta demanda.</p>
            <p><strong>Tecnología de punta:</strong></p>
            <ul>
                <li>LEDs RGB para espectro personalizable</li>
                <li>Control vía app Bluetooth</li>
                <li>Simulación de amanecer y atardecer</li>
                <li>Potencia ajustable para cualquier tipo de planta</li>
            </ul>''',
            'presentaciones': [
                {'nombre': 'Vivid 2 (30cm)', 'precio': Decimal('149.90')},
                {'nombre': 'Vivid 2 (45cm)', 'precio': Decimal('189.90')},
                {'nombre': 'Vivid 2 (60cm)', 'precio': Decimal('229.90')},
            ]
        },
        {
            'nombre': 'Chihiros X Series',
            'categoria': lamparas,
            'marca': chihiros,
            'descripcion': '''<p>Lámpara LED premium con diseño innovador de brazos extensibles.</p>
            <p><strong>Diseño exclusivo:</strong></p>
            <ul>
                <li>Brazos telescópicos de acero inoxidable</li>
                <li>Altura ajustable para control de intensidad</li>
                <li>LEDs de última generación</li>
                <li>Ideal para acuascaping profesional</li>
            </ul>''',
            'presentaciones': [
                {'nombre': 'X120 (30cm)', 'precio': Decimal('89.90')},
                {'nombre': 'X180 (45cm)', 'precio': Decimal('119.90')},
                {'nombre': 'X240 (60cm)', 'precio': Decimal('149.90')},
                {'nombre': 'X300 (75cm)', 'precio': Decimal('179.90')},
            ]
        },
    ]
    
    productos_creados = 0
    presentaciones_creadas = 0
    
    for producto_data in productos_data:
        # Verificar si el producto ya existe
        if Producto.objects.filter(nombre=producto_data['nombre']).exists():
            print(f"⚠️  Producto '{producto_data['nombre']}' ya existe. Saltando...")
            continue
        
        # Crear el producto
        producto = Producto.objects.create(
            nombre=producto_data['nombre'],
            categoria=producto_data['categoria'],
            marca=producto_data['marca'],
            descripcion=producto_data['descripcion'],
            activo=True,
            destacado=False,
        )
        productos_creados += 1
        print(f"✅ Producto creado: {producto.nombre}")
        
        # Crear las presentaciones
        for i, pres_data in enumerate(producto_data['presentaciones']):
            Presentacion.objects.create(
                producto=producto,
                nombre=pres_data['nombre'],
                precio=pres_data['precio'],
                stock=50,  # Stock inicial de ejemplo
                orden=i,
            )
            presentaciones_creadas += 1
        
        print(f"   └── {len(producto_data['presentaciones'])} presentaciones creadas")
    
    print(f"\n{'='*50}")
    print(f"📊 Resumen:")
    print(f"   - Productos creados: {productos_creados}")
    print(f"   - Presentaciones creadas: {presentaciones_creadas}")
    print(f"{'='*50}")


if __name__ == '__main__':
    print("🐠 Agregando productos a GardenAqua...\n")
    crear_productos()
    print("\n✨ Proceso completado!")
