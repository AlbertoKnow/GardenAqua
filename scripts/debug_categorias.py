"""Script para depurar categorías y productos."""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gardenaqua.settings')
django.setup()

from apps.catalogo.models import Categoria, Producto

print('=== CATEGORIAS ===')
for c in Categoria.objects.all().order_by('categoria_padre_id', 'nombre'):
    print(f'{c.id} | {c.nombre} | slug={c.slug} | padre_id={c.categoria_padre_id} | activo={c.activo}')

print()
print('=== PRODUCTOS Y SUS CATEGORIAS ===')
for p in Producto.objects.all():
    pres_count = p.presentaciones.filter(activo=True).count()
    print(f'{p.nombre} | cat={p.categoria.nombre} (id={p.categoria_id}) | activo={p.activo} | pres_activas={pres_count}')

print()
print('=== TEST: Filtrar productos de Filtros ===')
filtros = Categoria.objects.filter(slug='filtros').first()
if filtros:
    print(f'Categoria Filtros encontrada: ID={filtros.id}')
    categorias_ids = [filtros.id]
    subcategorias = filtros.subcategorias.filter(activo=True)
    print(f'Subcategorias activas: {list(subcategorias.values_list("id", "nombre"))}')
    if subcategorias.exists():
        categorias_ids.extend(subcategorias.values_list('id', flat=True))
    print(f'IDs a buscar: {categorias_ids}')
    
    productos = Producto.objects.filter(
        activo=True,
        presentaciones__activo=True,
        categoria_id__in=categorias_ids
    ).distinct()
    print(f'Productos encontrados: {productos.count()}')
    for p in productos:
        print(f'  - {p.nombre}')
else:
    print('No se encontro categoria Filtros')
