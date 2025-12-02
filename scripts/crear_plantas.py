"""
Script para crear plantas de Tropica con diferentes subcategorías.
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, '/app')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gardenaqua.settings')
django.setup()

from apps.catalogo.models import Categoria, Marca, Producto, Presentacion, EspecificacionProducto

# 1. Obtener o crear categoría principal "Plantas"
plantas_cat, created = Categoria.objects.get_or_create(
    nombre='Plantas',
    defaults={'descripcion': 'Plantas naturales para acuarios', 'activo': True}
)
print(f"{'✅ Creada' if created else '📌 Existente'}: {plantas_cat.nombre} [Principal]")

# 2. Crear subcategorías de plantas
subcategorias_plantas = [
    {
        'nombre': 'Plantas de Fondo',
        'descripcion': 'Plantas altas ideales para la parte trasera del acuario'
    },
    {
        'nombre': 'Plantas de Medio',
        'descripcion': 'Plantas de altura media para la zona central del acuario'
    },
    {
        'nombre': 'Plantas de Primer Plano',
        'descripcion': 'Plantas pequeñas o tapizantes para el frente del acuario'
    },
    {
        'nombre': 'Musgos y Helechos',
        'descripcion': 'Musgos, helechos y plantas epífitas para decorar troncos y rocas'
    },
]

subcats = {}
print("\n=== SUBCATEGORÍAS DE PLANTAS ===")
for subcat_data in subcategorias_plantas:
    subcat, created = Categoria.objects.get_or_create(
        nombre=subcat_data['nombre'],
        defaults={
            'descripcion': subcat_data['descripcion'],
            'categoria_padre': plantas_cat,
            'activo': True
        }
    )
    subcats[subcat_data['nombre']] = subcat
    print(f"  {'✅ Creada' if created else '📌 Existente'}: {subcat.nombre}")

# 3. Obtener marca Tropica
tropica, created = Marca.objects.get_or_create(
    nombre='Tropica',
    defaults={'descripcion': 'Líder mundial en plantas de acuario', 'activo': True}
)
print(f"\n{'✅ Creada' if created else '📌 Existente'}: Marca {tropica.nombre}")

# 4. Definir plantas por subcategoría
plantas = [
    # === PLANTAS DE FONDO ===
    {
        'nombre': 'Vallisneria Spiralis',
        'subcategoria': 'Plantas de Fondo',
        'descripcion_corta': 'Planta de fondo resistente con hojas en forma de cinta',
        'descripcion': '''<p>La <strong>Vallisneria Spiralis</strong> es una planta clásica de acuario, perfecta para principiantes.</p>
<p>Sus hojas largas y onduladas crean un hermoso efecto de movimiento con la corriente del agua. Crece rápidamente y se reproduce mediante estolones.</p>
<p><strong>Ideal para:</strong></p>
<ul>
<li>Acuarios de principiantes</li>
<li>Acuarios con peces vivíparos</li>
<li>Crear cortinas verdes en el fondo</li>
</ul>''',
        'presentaciones': [
            {'nombre': 'Porción', 'precio': 12.00},
            {'nombre': 'Maceta', 'precio': 25.00},
        ],
        'specs': [
            ('Dificultad', 'Fácil'),
            ('Luz requerida', 'Baja a Media'),
            ('CO2', 'No necesario'),
            ('Crecimiento', 'Rápido'),
            ('Altura', '20-60 cm'),
            ('Origen', 'Cosmopolita'),
        ]
    },
    {
        'nombre': 'Echinodorus Bleheri',
        'subcategoria': 'Plantas de Fondo',
        'descripcion_corta': 'Espada amazónica grande y robusta',
        'descripcion': '''<p>El <strong>Echinodorus Bleheri</strong>, conocido como "Espada Amazónica", es una de las plantas más populares en acuariofilia.</p>
<p>Sus grandes hojas verdes crean un impresionante punto focal en cualquier acuario. Muy resistente y fácil de mantener.</p>''',
        'presentaciones': [
            {'nombre': 'Maceta', 'precio': 35.00},
        ],
        'specs': [
            ('Dificultad', 'Fácil'),
            ('Luz requerida', 'Media'),
            ('CO2', 'Recomendado'),
            ('Crecimiento', 'Medio'),
            ('Altura', '20-50 cm'),
            ('Origen', 'Sudamérica'),
        ]
    },
    
    # === PLANTAS DE MEDIO ===
    {
        'nombre': 'Cryptocoryne Wendtii Green',
        'subcategoria': 'Plantas de Medio',
        'descripcion_corta': 'Cryptocoryne verde resistente para zona media',
        'descripcion': '''<p>La <strong>Cryptocoryne Wendtii Green</strong> es una planta muy versátil y resistente, ideal para la zona media del acuario.</p>
<p>Sus hojas onduladas de color verde intenso aportan textura y naturalidad. Muy tolerante a diferentes condiciones de agua.</p>''',
        'presentaciones': [
            {'nombre': 'Maceta', 'precio': 28.00},
            {'nombre': 'Porción (3-5 plantas)', 'precio': 18.00},
        ],
        'specs': [
            ('Dificultad', 'Fácil'),
            ('Luz requerida', 'Baja a Media'),
            ('CO2', 'No necesario'),
            ('Crecimiento', 'Lento'),
            ('Altura', '10-25 cm'),
            ('Origen', 'Sri Lanka'),
        ]
    },
    {
        'nombre': 'Anubias Barteri',
        'subcategoria': 'Plantas de Medio',
        'descripcion_corta': 'Anubias robusta de hojas anchas',
        'descripcion': '''<p>La <strong>Anubias Barteri</strong> es una planta extremadamente resistente y de crecimiento lento.</p>
<p>Perfecta para acuarios con peces herbívoros ya que sus hojas duras no son apetecibles. Se puede atar a rocas o troncos.</p>
<p><strong>Importante:</strong> No enterrar el rizoma, solo las raíces.</p>''',
        'presentaciones': [
            {'nombre': 'Maceta', 'precio': 38.00},
            {'nombre': 'Atada a roca', 'precio': 45.00},
        ],
        'specs': [
            ('Dificultad', 'Muy fácil'),
            ('Luz requerida', 'Baja'),
            ('CO2', 'No necesario'),
            ('Crecimiento', 'Muy lento'),
            ('Altura', '10-25 cm'),
            ('Origen', 'África Occidental'),
        ]
    },
    
    # === PLANTAS DE PRIMER PLANO ===
    {
        'nombre': 'Eleocharis Parvula',
        'subcategoria': 'Plantas de Primer Plano',
        'descripcion_corta': 'Planta tapizante tipo césped',
        'descripcion': '''<p>La <strong>Eleocharis Parvula</strong> es una planta tapizante que crea un efecto de césped en el acuario.</p>
<p>Forma una alfombra verde densa cuando se le proporcionan las condiciones adecuadas. Ideal para acuarios plantados estilo Nature Aquarium.</p>''',
        'presentaciones': [
            {'nombre': 'Maceta', 'precio': 22.00},
            {'nombre': 'Porción', 'precio': 15.00},
        ],
        'specs': [
            ('Dificultad', 'Media'),
            ('Luz requerida', 'Alta'),
            ('CO2', 'Recomendado'),
            ('Crecimiento', 'Medio'),
            ('Altura', '3-10 cm'),
            ('Origen', 'Cosmopolita'),
        ]
    },
    {
        'nombre': 'Staurogyne Repens',
        'subcategoria': 'Plantas de Primer Plano',
        'descripcion_corta': 'Planta compacta de hojas pequeñas',
        'descripcion': '''<p>La <strong>Staurogyne Repens</strong> es una planta de primer plano compacta y atractiva.</p>
<p>Sus pequeñas hojas verdes forman arbustos densos. Relativamente fácil de mantener comparada con otras plantas de primer plano.</p>''',
        'presentaciones': [
            {'nombre': 'Maceta', 'precio': 25.00},
        ],
        'specs': [
            ('Dificultad', 'Media'),
            ('Luz requerida', 'Media a Alta'),
            ('CO2', 'Recomendado'),
            ('Crecimiento', 'Medio'),
            ('Altura', '5-10 cm'),
            ('Origen', 'Brasil'),
        ]
    },
    
    # === MUSGOS Y HELECHOS ===
    {
        'nombre': 'Musgo de Java (Taxiphyllum Barbieri)',
        'subcategoria': 'Musgos y Helechos',
        'descripcion_corta': 'Musgo versátil y resistente para decoración',
        'descripcion': '''<p>El <strong>Musgo de Java</strong> es uno de los musgos más populares y fáciles de mantener en acuariofilia.</p>
<p>Se adhiere naturalmente a rocas, troncos y decoraciones. Excelente refugio para alevines y camarones.</p>''',
        'presentaciones': [
            {'nombre': 'Porción', 'precio': 15.00},
            {'nombre': 'Atado a tronco', 'precio': 35.00},
            {'nombre': 'Atado a roca', 'precio': 30.00},
        ],
        'specs': [
            ('Dificultad', 'Muy fácil'),
            ('Luz requerida', 'Baja'),
            ('CO2', 'No necesario'),
            ('Crecimiento', 'Lento a Medio'),
            ('Altura', '3-10 cm'),
            ('Origen', 'Sudeste Asiático'),
        ]
    },
    {
        'nombre': 'Helecho de Java (Microsorum Pteropus)',
        'subcategoria': 'Musgos y Helechos',
        'descripcion_corta': 'Helecho resistente de hojas alargadas',
        'descripcion': '''<p>El <strong>Helecho de Java</strong> es una planta epífita muy resistente y decorativa.</p>
<p>Sus hojas alargadas y texturizadas aportan un aspecto natural al acuario. No requiere sustrato, se ata a rocas o troncos.</p>
<p><strong>Nota:</strong> No enterrar el rizoma.</p>''',
        'presentaciones': [
            {'nombre': 'Maceta', 'precio': 32.00},
            {'nombre': 'Atado a tronco', 'precio': 48.00},
        ],
        'specs': [
            ('Dificultad', 'Muy fácil'),
            ('Luz requerida', 'Baja a Media'),
            ('CO2', 'No necesario'),
            ('Crecimiento', 'Lento'),
            ('Altura', '15-30 cm'),
            ('Origen', 'Sudeste Asiático'),
        ]
    },
]

# 5. Crear productos
print("\n=== CREANDO PLANTAS ===")
for planta_data in plantas:
    subcat = subcats[planta_data['subcategoria']]
    
    producto, created = Producto.objects.get_or_create(
        nombre=planta_data['nombre'],
        defaults={
            'categoria': subcat,
            'marca': tropica,
            'descripcion_corta': planta_data['descripcion_corta'],
            'descripcion': planta_data['descripcion'],
            'activo': True,
            'destacado': True,
        }
    )
    
    if created:
        print(f"\n✅ {producto.nombre}")
        print(f"   Subcategoría: {subcat.nombre}")
        
        # Crear presentaciones
        for i, pres_data in enumerate(planta_data['presentaciones']):
            sku_base = producto.slug.replace('-', '').upper()[:8]
            presentacion = Presentacion.objects.create(
                producto=producto,
                nombre=pres_data['nombre'],
                sku=f"{sku_base}-{i+1:03d}",
                precio=pres_data['precio'],
                stock=20,
                activo=True,
                orden=i
            )
            print(f"   └── {presentacion.nombre}: S/{presentacion.precio}")
        
        # Crear especificaciones
        for i, (nombre_spec, valor_spec) in enumerate(planta_data['specs']):
            EspecificacionProducto.objects.create(
                producto=producto,
                nombre=nombre_spec,
                valor=valor_spec,
                orden=i
            )
        print(f"   └── {len(planta_data['specs'])} especificaciones añadidas")
    else:
        print(f"\n📌 Ya existe: {producto.nombre}")

# Resumen final
print("\n" + "="*50)
print("✅ ¡PROCESO COMPLETADO!")
print("="*50)

print("\n📊 RESUMEN:")
print(f"\nCategoría principal: {plantas_cat.nombre}")
print(f"Subcategorías creadas: {len(subcats)}")
for nombre, subcat in subcats.items():
    count = Producto.objects.filter(categoria=subcat).count()
    print(f"  └── {nombre}: {count} productos")

print(f"\nMarca: {tropica.nombre}")
print(f"Total plantas creadas: {Producto.objects.filter(categoria__categoria_padre=plantas_cat).count()}")
