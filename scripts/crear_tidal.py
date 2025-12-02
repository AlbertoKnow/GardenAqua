"""
Script para crear los filtros Tidal de Seachem como ejemplo.
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, '/app')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gardenaqua.settings')
django.setup()

from apps.catalogo.models import Categoria, Marca, Producto, Presentacion, EspecificacionProducto

# Mostrar datos existentes
print("=== CATEGORÍAS EXISTENTES ===")
for c in Categoria.objects.all():
    padre = f" (Padre: {c.categoria_padre.nombre})" if c.categoria_padre else " [Principal]"
    print(f"  {c.id}: {c.nombre}{padre}")

print("\n=== MARCAS EXISTENTES ===")
for m in Marca.objects.all():
    print(f"  {m.id}: {m.nombre}")

# 1. Crear categoría "Filtros" si no existe
filtros_cat, created = Categoria.objects.get_or_create(
    nombre='Filtros',
    defaults={'descripcion': 'Filtros para acuarios', 'activo': True}
)
if created:
    print(f"\n✅ Categoría creada: {filtros_cat.nombre}")
else:
    print(f"\n📌 Categoría existente: {filtros_cat.nombre}")

# 2. Crear subcategoría "Filtros de Cascada (HOB)"
hob_cat, created = Categoria.objects.get_or_create(
    nombre='Filtros de Cascada (HOB)',
    defaults={
        'descripcion': 'Filtros Hang On Back para acuarios',
        'categoria_padre': filtros_cat,
        'activo': True
    }
)
if created:
    print(f"✅ Subcategoría creada: {hob_cat.nombre}")
else:
    print(f"📌 Subcategoría existente: {hob_cat.nombre}")

# 3. Crear marca "Seachem" si no existe
seachem, created = Marca.objects.get_or_create(
    nombre='Seachem',
    defaults={'descripcion': 'Marca líder en productos para acuarios', 'activo': True}
)
if created:
    print(f"✅ Marca creada: {seachem.nombre}")
else:
    print(f"📌 Marca existente: {seachem.nombre}")

# 4. Definir los 4 modelos Tidal con sus especificaciones
tidal_models = [
    {
        'nombre': 'Filtro Tidal 35 Seachem',
        'descripcion_corta': 'Filtro de cascada para acuarios hasta 130 litros',
        'descripcion': '''<p>El <strong>Seachem Tidal 35</strong> es un filtro de cascada (HOB) de alta calidad diseñado para acuarios de hasta 130 litros.</p>
<p>Características principales:</p>
<ul>
<li>Sistema de auto-cebado</li>
<li>Cesta de medios extraíble</li>
<li>Flujo ajustable</li>
<li>Indicador de mantenimiento</li>
<li>Motor silencioso y eficiente</li>
</ul>''',
        'precio': 250.00,
        'specs': [
            ('Caudal máximo', '350 L/h'),
            ('Capacidad del acuario', 'Hasta 130 litros'),
            ('Volumen de la cesta', '0.75 litros'),
            ('Potencia', '6W'),
            ('Dimensiones', '15 x 18 x 20 cm'),
        ]
    },
    {
        'nombre': 'Filtro Tidal 55 Seachem',
        'descripcion_corta': 'Filtro de cascada para acuarios hasta 200 litros',
        'descripcion': '''<p>El <strong>Seachem Tidal 55</strong> es un filtro de cascada (HOB) de alta calidad diseñado para acuarios de hasta 200 litros.</p>
<p>Características principales:</p>
<ul>
<li>Sistema de auto-cebado</li>
<li>Cesta de medios extraíble</li>
<li>Flujo ajustable</li>
<li>Indicador de mantenimiento</li>
<li>Motor silencioso y eficiente</li>
</ul>''',
        'precio': 320.00,
        'specs': [
            ('Caudal máximo', '550 L/h'),
            ('Capacidad del acuario', 'Hasta 200 litros'),
            ('Volumen de la cesta', '1.0 litros'),
            ('Potencia', '8W'),
            ('Dimensiones', '17 x 20 x 22 cm'),
        ]
    },
    {
        'nombre': 'Filtro Tidal 75 Seachem',
        'descripcion_corta': 'Filtro de cascada para acuarios hasta 300 litros',
        'descripcion': '''<p>El <strong>Seachem Tidal 75</strong> es un filtro de cascada (HOB) de alta calidad diseñado para acuarios de hasta 300 litros.</p>
<p>Características principales:</p>
<ul>
<li>Sistema de auto-cebado</li>
<li>Cesta de medios extraíble</li>
<li>Flujo ajustable</li>
<li>Indicador de mantenimiento</li>
<li>Motor silencioso y eficiente</li>
</ul>''',
        'precio': 400.00,
        'specs': [
            ('Caudal máximo', '750 L/h'),
            ('Capacidad del acuario', 'Hasta 300 litros'),
            ('Volumen de la cesta', '1.5 litros'),
            ('Potencia', '10W'),
            ('Dimensiones', '19 x 22 x 25 cm'),
        ]
    },
    {
        'nombre': 'Filtro Tidal 110 Seachem',
        'descripcion_corta': 'Filtro de cascada para acuarios hasta 450 litros',
        'descripcion': '''<p>El <strong>Seachem Tidal 110</strong> es un filtro de cascada (HOB) de alta calidad diseñado para acuarios de hasta 450 litros.</p>
<p>Características principales:</p>
<ul>
<li>Sistema de auto-cebado</li>
<li>Cesta de medios extraíble</li>
<li>Flujo ajustable</li>
<li>Indicador de mantenimiento</li>
<li>Motor silencioso y eficiente</li>
</ul>''',
        'precio': 500.00,
        'specs': [
            ('Caudal máximo', '1100 L/h'),
            ('Capacidad del acuario', 'Hasta 450 litros'),
            ('Volumen de la cesta', '2.0 litros'),
            ('Potencia', '15W'),
            ('Dimensiones', '22 x 25 x 28 cm'),
        ]
    },
]

# 5. Crear cada producto Tidal
print("\n=== CREANDO PRODUCTOS TIDAL ===")
for tidal in tidal_models:
    producto, created = Producto.objects.get_or_create(
        nombre=tidal['nombre'],
        defaults={
            'categoria': hob_cat,
            'marca': seachem,
            'descripcion_corta': tidal['descripcion_corta'],
            'descripcion': tidal['descripcion'],
            'activo': True,
            'destacado': True,
        }
    )
    
    if created:
        print(f"✅ Producto creado: {producto.nombre}")
        
        # Crear presentación (solo "Unidad" para filtros)
        presentacion = Presentacion.objects.create(
            producto=producto,
            nombre='Unidad',
            sku=f"TIDAL-{tidal['nombre'].split()[2]}-001",
            precio=tidal['precio'],
            stock=10,
            activo=True
        )
        print(f"   └── Presentación: {presentacion.nombre} - S/{presentacion.precio}")
        
        # Crear especificaciones
        for i, (nombre_spec, valor_spec) in enumerate(tidal['specs']):
            EspecificacionProducto.objects.create(
                producto=producto,
                nombre=nombre_spec,
                valor=valor_spec,
                orden=i
            )
            print(f"   └── Spec: {nombre_spec}: {valor_spec}")
    else:
        print(f"📌 Producto existente: {producto.nombre}")

print("\n✅ ¡Proceso completado!")
print("\n=== RESUMEN ===")
print(f"Categoría padre: {filtros_cat.nombre} (ID: {filtros_cat.id})")
print(f"Subcategoría: {hob_cat.nombre} (ID: {hob_cat.id})")
print(f"Marca: {seachem.nombre} (ID: {seachem.id})")
print(f"Productos Tidal creados: {Producto.objects.filter(nombre__contains='Tidal').count()}")
