# 🐠 TuAcuario - E-commerce para Tiendas de Acuarios

Sistema de e-commerce completo y profesional diseñado para tiendas de acuarios y productos acuáticos. Desarrollado con Django, PostgreSQL y Docker.

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Django](https://img.shields.io/badge/Django-5.2-green)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🎯 Descripción

**TuAcuario** es una solución e-commerce lista para producción, diseñada específicamente para negocios del sector acuarista. Incluye gestión de catálogo con categorías jerárquicas, múltiples presentaciones por producto, carrito de compras, sistema de pedidos con notificaciones y un panel de administración intuitivo.

### 🖼️ Capturas de Pantalla

> *Añade aquí capturas de tu proyecto desplegado*

---

## ✨ Características Principales

### 📦 Catálogo de Productos
- Categorías y subcategorías jerárquicas
- Múltiples marcas
- Presentaciones con diferentes precios y stock
- Galería de imágenes por producto
- Conversión automática a WebP para optimización
- Filtros por categoría, marca y búsqueda

### 🛒 Carrito de Compras
- Basado en sesiones (sin registro obligatorio)
- Actualización de cantidades en tiempo real
- Persistencia durante la navegación

### 📋 Sistema de Pedidos
- Checkout simplificado
- Seguimiento por código único
- Estados: Pendiente → Confirmado → Enviado → Entregado
- Historial de cambios de estado

### 📧 Notificaciones
- Email de confirmación al cliente (Resend API)
- Notificación al administrador
- Integración con WhatsApp

### 🎨 Diseño
- Tema minimalista monocromático
- Responsive (móvil, tablet, desktop)
- Bootstrap 5.3
- Fuente Poppins

### 🔧 Administración
- Panel Django Admin personalizado
- Gestión completa de productos, categorías y pedidos
- Editor de texto enriquecido (CKEditor 5)

---

## 🛠️ Stack Tecnológico

| Categoría | Tecnología |
|-----------|------------|
| **Backend** | Python 3.13, Django 5.2 |
| **Base de Datos** | PostgreSQL 16 (prod), SQLite (dev) |
| **Servidor Web** | Nginx + Gunicorn |
| **Contenedores** | Docker, Docker Compose |
| **Imágenes** | Pillow (conversión WebP) |
| **Email** | Resend API |
| **Frontend** | Django Templates, Bootstrap 5.3 |
| **SSL** | Certificados personalizados |

---

## 📦 Requisitos

### Desarrollo Local
- Python 3.11+
- pip
- Git

### Producción (Docker)
- Docker Engine 20.10+
- Docker Compose 2.0+
- VPS con 1GB RAM mínimo

---

## 🚀 Instalación

### Desarrollo Local

```bash
# Clonar repositorio
git clone https://github.com/tu-usuario/tuacuario.git
cd tuacuario

# Crear entorno virtual
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus valores

# Migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Ejecutar servidor
python manage.py runserver
```

### Producción (Docker)

```bash
# Configurar variables de entorno
cp .env.production.example .env

# Construir y ejecutar
docker compose up -d --build

# Crear superusuario
docker exec -it tuacuario_web python manage.py createsuperuser
```

---

## ⚙️ Variables de Entorno

```env
# Django
DJANGO_SECRET_KEY=tu-clave-secreta-muy-larga
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=tudominio.com,www.tudominio.com

# Base de datos
DB_NAME=tuacuario
DB_USER=tuacuario
DB_PASSWORD=contraseña-segura
DB_HOST=db
DB_PORT=5432

# Email (Resend)
RESEND_API_KEY=re_xxxxxxxxxxxx
RESEND_FROM_EMAIL=TuAcuario <pedidos@tudominio.com>
ADMIN_EMAIL=admin@tudominio.com

# Sitio
SITE_NAME=TuAcuario
SITE_URL=https://tudominio.com
WHATSAPP_NUMBER=51999999999
```

---

## 📁 Estructura del Proyecto

```
tuacuario/
├── apps/
│   ├── catalogo/       # Productos, categorías, marcas
│   ├── carrito/        # Carrito de compras
│   └── pedidos/        # Gestión de pedidos
├── gardenaqua/         # Configuración Django
├── templates/          # Plantillas HTML
├── static/             # Archivos estáticos
├── media/              # Archivos subidos
├── nginx/              # Configuración Nginx
├── scripts/            # Scripts de utilidad
├── docker-compose.yml  # Orquestación Docker
├── Dockerfile          # Imagen Docker
└── requirements.txt    # Dependencias Python
```

---

## 🔧 Comandos Útiles

```bash
# Logs del contenedor
docker logs tuacuario_web -f

# Shell de Django
docker exec -it tuacuario_web python manage.py shell

# Migraciones
docker exec -it tuacuario_web python manage.py migrate

# Recolectar estáticos
docker exec -it tuacuario_web python manage.py collectstatic --noinput
```

---

## 🎨 Personalización

### Cambiar Logo
Reemplaza `static/img/logo.webp` con tu logo (formato WebP recomendado).

### Colores
Edita las variables CSS en `templates/base.html`:
```css
:root {
    --color-primary: #111111;
    --color-accent: #333333;
    /* ... */
}
```

### Información de Contacto
Actualiza en `templates/base.html`:
- WhatsApp
- Email
- Redes sociales

---

## 📈 Características Futuras

- [ ] Pasarela de pagos (Mercado Pago, PayPal)
- [ ] Sistema de usuarios registrados
- [ ] Wishlist / Favoritos
- [ ] Cupones de descuento
- [ ] Reviews de productos
- [ ] Integración con inventario

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/nueva-caracteristica`)
3. Commit tus cambios (`git commit -m 'Añadir nueva característica'`)
4. Push a la rama (`git push origin feature/nueva-caracteristica`)
5. Abre un Pull Request

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver [LICENSE.MD](LICENSE.MD) para más detalles.

---

## 👨‍💻 Autor

Desarrollado por **Alberto** - [GitHub](https://github.com/AlbertoKnow)

---

## 💼 Contacto Profesional

¿Interesado en un proyecto similar o personalización?

- 📧 Email: luis.huamani.dev@gmail.com
- 💼 LinkedIn: https://www.linkedin.com/in/luis-huaman%C3%AD/
- 🐙 GitHub: [@AlbertoKnow](https://github.com/AlbertoKnow)

---

<p align="center">
  <sub>Hecho con ❤️ y Django</sub>
</p>
