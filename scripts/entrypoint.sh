#!/bin/bash
# =============================================================================
# Script de entrada para el contenedor de GardenAqua
# =============================================================================
# Ejecuta migraciones y luego inicia Gunicorn

set -e

echo "🚀 Iniciando GardenAqua..."

# Esperar a que la base de datos esté lista
echo "⏳ Esperando a la base de datos..."
while ! python -c "import django; django.setup(); from django.db import connection; connection.ensure_connection()" 2>/dev/null; do
    sleep 1
done
echo "✅ Base de datos lista"

# Ejecutar migraciones
echo "📦 Ejecutando migraciones..."
python manage.py migrate --noinput

# Recolectar archivos estáticos
echo "📁 Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

# Iniciar Gunicorn
echo "🌐 Iniciando servidor Gunicorn..."
exec gunicorn --bind 0.0.0.0:8000 --workers 3 --access-logfile - --error-logfile - gardenaqua.wsgi:application
