# E-Commerce - Entrega Final de Portafolio

Aplicación web de comercio electrónico con flujo completo: catálogo, carrito de compras, confirmación de pedidos y administración de productos. Desarrollada con Django y PostgreSQL como proyecto final del Bootcamp Full Stack Python (PF1478), Módulo 8.

## Repositorio

> **Enlace público:** https://github.com/rodrigohb/ecommerce-final  
> *(actualizar con la URL real del repositorio)*

## Tecnologías

- Python 3.12
- Django 4.2
- PostgreSQL 17
- Bootstrap 5.3
- Bootstrap Icons
- HTML5 / CSS3

## Funcionalidades

**Catálogo público:**
- Listado de productos con tarjetas visuales
- Filtrado por categoría (se mantiene al paginar)
- Detalle de producto con stock disponible
- Paginación

**Carrito de compras (cliente autenticado):**
- Agregar productos desde el detalle
- Actualizar cantidades
- Eliminar productos
- Subtotales por línea y total general
- Validación de stock disponible

**Órdenes / Compra:**
- Checkout con resumen del pedido
- Confirmación que registra la orden con sus ítems
- Orden asociada al usuario autenticado
- Descuento automático de stock al confirmar
- Historial de pedidos por usuario

**Autenticación y roles:**
- Login / Logout
- Registro de nuevos usuarios (clientes)
- Rol ADMIN: accede a panel de administración de productos (CRUD)
- Rol CLIENTE: accede a catálogo, carrito y compras
- Vistas protegidas con @login_required y @staff_member_required

**Validaciones y mensajes:**
- Validación en formularios (nombre >= 3 chars, precio > 0, stock >= 0)
- Validación de cantidades vs stock en carrito
- Mensajes de éxito/error/info con framework de messages de Django

**Administración:**
- Panel de admin de productos con tabla (solo staff)
- Django Admin personalizado con inlines para órdenes

## Requisitos previos

- Python 3.10 o superior
- PostgreSQL instalado y corriendo
- pip

## Instalación

```bash
# 1. Clonar repositorio
git clone https://github.com/rodrigohb/ecommerce-final.git
cd ecommerce_project

# 2. Crear y activar entorno virtual
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Editar .env con datos de PostgreSQL

# 5. Crear base de datos en PostgreSQL
# psql -U postgres
# CREATE DATABASE ecommerce_final_db;
# \q

# 6. Aplicar migraciones
python manage.py makemigrations catalogo ordenes
python manage.py migrate

# 7. Cargar datos de prueba (categorías, productos, usuarios)
python manage.py cargar_datos

# 8. Ejecutar servidor
python manage.py runserver
```

Abrir en el navegador: http://127.0.0.1:8000/

## Credenciales de prueba

| Rol | Usuario | Contraseña | Acceso |
|-----|---------|------------|--------|
| **ADMIN** | `admin1` | `admin1234` | Catálogo + Carrito + Admin Productos + Django Admin |
| **CLIENTE** | `cliente1` | `cliente1234` | Catálogo + Carrito + Compras + Mis Pedidos |

## Rutas principales

**Públicas (sin autenticación):**

| Ruta | Descripción |
|------|-------------|
| `/` | Catálogo de productos |
| `/producto/<id>/` | Detalle de producto |
| `/login/` | Iniciar sesión |
| `/registro/` | Crear cuenta nueva |

**Cliente autenticado:**

| Ruta | Descripción |
|------|-------------|
| `/carrito/` | Ver carrito de compras |
| `/carrito/agregar/<id>/` | Agregar producto al carrito |
| `/ordenes/checkout/` | Confirmar compra |
| `/ordenes/confirmacion/<id>/` | Confirmación de orden |
| `/ordenes/mis-ordenes/` | Historial de pedidos |

**Solo administrador (staff):**

| Ruta | Descripción |
|------|-------------|
| `/admin-productos/` | Panel de administración de productos |
| `/producto/crear/` | Crear nuevo producto |
| `/producto/<id>/editar/` | Editar producto |
| `/producto/<id>/eliminar/` | Eliminar producto |
| `/admin/` | Django Admin |

## Estructura del proyecto

```
ecommerce_project/
├── ecommerce_project/          # Configuración del proyecto
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── catalogo/                   # App: productos y categorías
│   ├── management/commands/
│   │   └── cargar_datos.py     # Seed de datos + usuarios
│   ├── templatetags/
│   │   └── catalogo_filters.py # Filtro formato CLP
│   ├── models.py               # Categoria, Producto
│   ├── views.py                # CRUD + registro
│   ├── forms.py                # ProductoForm, RegistroForm
│   ├── urls.py
│   └── admin.py
├── carrito/                    # App: carrito de compras (sesión)
│   ├── carrito.py              # Lógica del carrito
│   ├── context_processors.py   # Badge en navbar
│   ├── views.py                # Agregar/quitar/actualizar
│   └── urls.py
├── ordenes/                    # App: órdenes de compra
│   ├── models.py               # Orden, OrdenItem
│   ├── views.py                # Checkout, confirmación
│   ├── urls.py
│   └── admin.py
├── templates/                  # Templates globales
│   ├── base.html
│   ├── catalogo/
│   ├── carrito/
│   ├── ordenes/
│   └── registration/
├── static/css/
├── .env.example
├── .gitignore
├── requirements.txt
├── manage.py
└── README.md
```

## Flujo principal

1. Usuario visita el catálogo (`/`)
2. Puede filtrar por categoría y ver detalle de productos
3. Se registra o inicia sesión
4. Agrega productos al carrito desde el detalle
5. Revisa el carrito: actualiza cantidades o elimina items
6. Confirma la compra en checkout
7. Se registra la orden, se descuenta stock, se limpia el carrito
8. Ve la confirmación y puede revisar su historial de pedidos

## Autor

Rodrigo Mondaca Irarrázabal - Bootcamp Full Stack Python 2026
