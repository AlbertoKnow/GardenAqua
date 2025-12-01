# =============================================================================
# Dockerfile para GardenAqua - Tienda Online
# =============================================================================
# Imagen multi-stage para optimizar el tamaño final

# -----------------------------------------------------------------------------
# Etapa 1: Base
# -----------------------------------------------------------------------------
FROM python:3.13-slim as base

# Variables de entorno para Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema necesarias para Pillow y PostgreSQL
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
    && rm -rf /var/lib/apt/lists/*

# -----------------------------------------------------------------------------
# Etapa 2: Dependencias
# -----------------------------------------------------------------------------
FROM base as dependencies

# Copiar requirements e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# -----------------------------------------------------------------------------
# Etapa 3: Producción
# -----------------------------------------------------------------------------
FROM dependencies as production

# Crear usuario no-root para seguridad
RUN useradd --create-home --shell /bin/bash appuser

# Copiar el código del proyecto
COPY --chown=appuser:appuser . .

# Copiar y dar permisos al script de entrada
COPY --chown=appuser:appuser scripts/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Crear directorios necesarios
RUN mkdir -p /app/staticfiles /app/media && \
    chown -R appuser:appuser /app/staticfiles /app/media

# Cambiar al usuario no-root
USER appuser

# Puerto de la aplicación
EXPOSE 8000

# Script de entrada
ENTRYPOINT ["/entrypoint.sh"]
