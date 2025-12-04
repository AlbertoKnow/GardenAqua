"""
Script principal para ejecutar todos los scripts de productos.
"""
import sys
import os

# Añadir el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tropical import agregar_productos_tropical
from seachem import agregar_productos_seachem
from chihiros import agregar_productos_chihiros
from week_aqua import agregar_productos_week_aqua
from azoo import agregar_productos_azoo, agregar_productos_azoo_plus
from aquario import agregar_productos_aquario


def ejecutar_todo():
    """Ejecuta todos los scripts de productos."""
    print("=" * 50)
    print("🐠 AGREGANDO PRODUCTOS A GARDENAQUA")
    print("=" * 50)
    
    print("\n📦 Marca: TROPICAL (Alimentos)")
    agregar_productos_tropical()
    
    print("\n📦 Marca: SEACHEM (Fertilizantes, Sustratos)")
    agregar_productos_seachem()
    
    print("\n📦 Marca: CHIHIROS (Lámparas)")
    agregar_productos_chihiros()
    
    print("\n📦 Marca: WEEK AQUA (Lámparas)")
    agregar_productos_week_aqua()
    
    print("\n📦 Marca: AZOO (Fertilizantes)")
    agregar_productos_azoo()
    
    print("\n📦 Marca: AZOO PLUS (Sustratos)")
    agregar_productos_azoo_plus()
    
    print("\n📦 Marca: AQUARIO (Sustratos, Fertilizantes)")
    agregar_productos_aquario()
    
    print("\n" + "=" * 50)
    print("✨ PROCESO COMPLETADO")
    print("=" * 50)


if __name__ == '__main__':
    ejecutar_todo()
