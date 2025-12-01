"""
Configuración de Django para el proyecto GardenAqua.

GardenAqua es una tienda online especializada en productos para acuarios y peces.
Este archivo contiene la configuración principal del proyecto Django.

Para más información sobre este archivo, ver:
https://docs.djangoproject.com/en/5.2/topics/settings/
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Ruta base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent


# =============================================================================
# CONFIGURACIÓN DE SEGURIDAD
# =============================================================================

# ADVERTENCIA: Mantener la clave secreta en producción segura
SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'django-insecure-imbwy0fyq08q-#=78#&hu@=n4%f=6!f11g+w#8&cnm%#yzp#!e'
)

# ADVERTENCIA: No ejecutar con DEBUG activado en producción
DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Orígenes confiables para CSRF (necesario cuando se usa proxy reverso)
CSRF_TRUSTED_ORIGINS = [
    f"http://{host}" for host in ALLOWED_HOSTS
] + [
    f"https://{host}" for host in ALLOWED_HOSTS
]


# =============================================================================
# DEFINICIÓN DE APLICACIONES
# =============================================================================

INSTALLED_APPS = [
    # Aplicaciones de Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Aplicaciones de terceros
    
    # Aplicaciones propias del proyecto
    'apps.catalogo',
    'apps.carrito',
    'apps.pedidos',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'gardenaqua.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.carrito.context_processors.carrito',
                'apps.catalogo.context_processors.categorias',
            ],
        },
    },
]

WSGI_APPLICATION = 'gardenaqua.wsgi.application'


# =============================================================================
# BASE DE DATOS
# =============================================================================
# Por defecto usamos SQLite para desarrollo, pero está preparado para PostgreSQL
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DB_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.environ.get('DB_NAME', BASE_DIR / 'db.sqlite3'),
        'USER': os.environ.get('DB_USER', ''),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', ''),
        'PORT': os.environ.get('DB_PORT', ''),
    }
}


# =============================================================================
# VALIDACIÓN DE CONTRASEÑAS
# =============================================================================
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# =============================================================================
# INTERNACIONALIZACIÓN
# =============================================================================
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'es-mx'

TIME_ZONE = 'America/Mexico_City'

USE_I18N = True

USE_TZ = True


# =============================================================================
# ARCHIVOS ESTÁTICOS Y MULTIMEDIA
# =============================================================================
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'


# =============================================================================
# CONFIGURACIÓN DE CAMPO DE CLAVE PRIMARIA
# =============================================================================
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# =============================================================================
# CONFIGURACIÓN DE EMAIL CON RESEND
# =============================================================================
# Usamos Resend como servicio de envío de emails transaccionales.
# Documentación: https://resend.com/docs

RESEND_API_KEY = os.environ.get('RESEND_API_KEY', '')
RESEND_FROM_EMAIL = os.environ.get('RESEND_FROM_EMAIL', 'GardenAqua <pedidos@gardenaqua.me>')
RESEND_REPLY_TO = os.environ.get('RESEND_REPLY_TO', '')

# Email donde GardenAqua recibe notificaciones de pedidos nuevos
ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', '')


# =============================================================================
# WHATSAPP
# =============================================================================
WHATSAPP_NUMBER = os.environ.get('WHATSAPP_NUMBER', '51916557975')


# =============================================================================
# CONFIGURACIÓN DEL SITIO
# =============================================================================

SITE_NAME = os.environ.get('SITE_NAME', 'GardenAqua')
SITE_URL = os.environ.get('SITE_URL', 'http://127.0.0.1:8000')
SITE_DESCRIPTION = 'Tu tienda especializada en acuarios y productos para peces'


# =============================================================================
# CONFIGURACIÓN DE PRODUCCIÓN
# =============================================================================
# Configuraciones adicionales para entorno de producción

if not DEBUG:
    # Seguridad HTTPS
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = os.environ.get('SECURE_SSL_REDIRECT', 'True') == 'True'
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    
    # HSTS
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    
    # WhiteNoise para archivos estáticos comprimidos
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    
    # Hosts de confianza para CSRF
    CSRF_TRUSTED_ORIGINS = [
        f"https://{host}" for host in ALLOWED_HOSTS if host not in ['localhost', '127.0.0.1']
    ]
