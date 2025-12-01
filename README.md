# 🐠 GardenAqua

Tienda online especializada en productos para acuarios y peces. Desarrollada con Django y desplegada con Docker.

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Django](https://img.shields.io/badge/Django-5.2-green)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Tecnologías](#-tecnologías)
- [Requisitos Previos](#-requisitos-previos)
- [Instalación Local](#-instalación-local)
- [Despliegue con Docker](#-despliegue-con-docker)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Variables de Entorno](#-variables-de-entorno)
- [Administración](#-administración)
- [Licencia](#-licencia)

---

## ✨ Características

- 🛒 **Catálogo de productos** con categorías y marcas
- 🖼️ **Galería de imágenes** con conversión automática a WebP
- 🛍️ **Carrito de compras** basado en sesiones
- 📦 **Sistema de pedidos** con seguimiento por código
- 📧 **Notificaciones por email** usando Resend API
- 📱 **Integración con WhatsApp** para consultas
- 🎨 **Diseño minimalista** monocromático (blanco/negro/gris)
- 🔐 **Panel de administración** Django Admin
- 🐳 **Dockerizado** para fácil despliegue

---

## 🛠️ Tecnologías

| Categoría | Tecnología |
|-----------|------------|
| Backend | Python 3.13, Django 5.2 |
| Base de Datos | PostgreSQL 16 (prod), SQLite (dev) |
| Servidor Web | Nginx + Gunicorn |
| Contenedores | Docker, Docker Compose |
| Procesamiento de Imágenes | Pillow (WebP) |
| Email | Resend API |
| Frontend | Django Templates, Bootstrap 5.3, Poppins Font |

---

## 📦 Requisitos Previos

### Para desarrollo local:
- Python 3.11+
- pip
- Git

### Para despliegue con Docker:
- Docker Engine 20.10+
- Docker Compose 2.0+

---

## 🚀 Instalación Local

### 1. Clonar el repositorio

```bash
git clone https://github.com/AlbertoKnow/GardenAqua.git
cd GardenAqua
```

### 2. Crear entorno virtual

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Crear archivo `.env` en la raíz del proyecto:

```env
DJANGO_SECRET_KEY=tu-clave-secreta-aqui
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Email (opcional)
RESEND_API_KEY=tu-api-key-de-resend
RESEND_FROM_EMAIL=tu-email@dominio.com

# WhatsApp (opcional)
WHATSAPP_NUMBER=51999999999
```

### 5. Ejecutar migraciones

```bash
python manage.py migrate
```

### 6. Crear superusuario

```bash
python manage.py createsuperuser
```

### 7. Ejecutar servidor de desarrollo

```bash
python manage.py runserver
```

Accede a:
- **Sitio web:** http://localhost:8000
- **Admin:** http://localhost:8000/admin/

---

## 🐳 Despliegue con Docker

### Desarrollo con Docker

```bash
# Construir y levantar contenedores
docker compose -f docker-compose.dev.yml up --build

# En segundo plano
docker compose -f docker-compose.dev.yml up -d --build
```

### Producción con Docker

#### 1. Crear archivo `.env.production`

```env
# Django
DJANGO_SECRET_KEY=genera-una-clave-secreta-segura
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com,localhost

# Base de datos
DB_NAME=gardenaqua
DB_USER=gardenaqua
DB_PASSWORD=tu-password-seguro

# Email
RESEND_API_KEY=tu-api-key
RESEND_FROM_EMAIL=GardenAqua <pedidos@tu-dominio.com>
ADMIN_EMAIL=admin@tu-dominio.com

# WhatsApp
WHATSAPP_NUMBER=51999999999

# Sitio
SITE_NAME=GardenAqua
SITE_URL=https://tu-dominio.com

# Seguridad (activar cuando tengas SSL)
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
ENABLE_HSTS=False
```

#### 2. Crear symlink para Docker Compose

```bash
ln -sf .env.production .env
```

#### 3. Levantar contenedores de producción

```bash
# Construir y levantar
docker compose up -d --build

# Ver logs
docker compose logs -f

# Ver estado de contenedores
docker compose ps
```

#### 4. Crear superusuario en producción

```bash
docker exec -it gardenaqua_web python manage.py createsuperuser
```

### Comandos útiles de Docker

```bash
# Detener contenedores
docker compose down

# Detener y eliminar volúmenes (¡CUIDADO! Borra datos)
docker compose down -v

# Reiniciar solo el contenedor web
docker compose restart web

# Ver logs del contenedor web
docker logs gardenaqua_web -f

# Ejecutar comando en contenedor
docker exec -it gardenaqua_web python manage.py shell
```

---

## 📁 Estructura del Proyecto

```
GardenAqua/
├── apps/
│   ├── catalogo/          # Productos, categorías, marcas
│   ├── carrito/           # Carrito de compras (sesiones)
│   └── pedidos/           # Pedidos y checkout
├── gardenaqua/            # Configuración del proyecto
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── templates/             # Plantillas HTML
│   ├── base.html
│   ├── catalogo/
│   ├── carrito/
│   └── pedidos/
├── static/                # Archivos estáticos
├── media/                 # Archivos subidos (imágenes)
├── nginx/                 # Configuración de Nginx
├── scripts/               # Scripts de utilidad
├── docker-compose.yml     # Docker Compose producción
├── docker-compose.dev.yml # Docker Compose desarrollo
├── Dockerfile             # Imagen Docker
├── requirements.txt       # Dependencias Python
└── README.md
```

---

## 🔧 Variables de Entorno

| Variable | Descripción | Requerido |
|----------|-------------|-----------|
| `DJANGO_SECRET_KEY` | Clave secreta de Django | ✅ Sí |
| `DJANGO_DEBUG` | Modo debug (True/False) | ✅ Sí |
| `DJANGO_ALLOWED_HOSTS` | Hosts permitidos (separados por coma) | ✅ Sí |
| `DB_ENGINE` | Motor de BD (postgresql/sqlite3) | No |
| `DB_NAME` | Nombre de la base de datos | Producción |
| `DB_USER` | Usuario de la BD | Producción |
| `DB_PASSWORD` | Contraseña de la BD | Producción |
| `DB_HOST` | Host de la BD | Producción |
| `DB_PORT` | Puerto de la BD | Producción |
| `RESEND_API_KEY` | API Key de Resend | No |
| `RESEND_FROM_EMAIL` | Email remitente | No |
| `WHATSAPP_NUMBER` | Número de WhatsApp | No |
| `SECURE_SSL_REDIRECT` | Redirigir a HTTPS | No |
| `SESSION_COOKIE_SECURE` | Cookies seguras | No |
| `CSRF_COOKIE_SECURE` | CSRF seguro | No |
| `ENABLE_HSTS` | Activar HSTS | No |

---

## 👤 Administración

### Acceso al panel de administración

- **URL:** `/admin/`
- **Funcionalidades:**
  - Gestionar categorías
  - Gestionar marcas
  - Gestionar productos y presentaciones
  - Gestionar imágenes de productos
  - Ver y gestionar pedidos
  - Actualizar estados de pedidos

### Conversión de imágenes a WebP

Las imágenes se convierten automáticamente a WebP al subirlas. Para convertir imágenes existentes:

```bash
python manage.py convertir_imagenes_webp
```

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE.MD](LICENSE.MD) para más detalles.

---

## 🤝 Contribuir

1. Fork el repositorio
2. Crea una rama (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'feat: agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

---

## 📞 Contacto

- **Sitio Web:** [gardenaqua.me](http://gardenaqua.me)
- **Email:** luis.huamani.dev@gmail.com

---

<p align="center">
  Hecho con ❤️ para GardenAqua
</p>
