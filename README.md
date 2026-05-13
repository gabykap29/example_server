# Example Server - FastAPI

Servidor API construido con **FastAPI** y **SQLModel** para probar endpoints y medir complejidad algorítmica. Incluye comparaciones de rendimiento entre distintas implementaciones (O(n) vs O(1), vectorizado con NumPy, Timsort vs SQL ORDER BY, etc.).

## Tecnologías

- **FastAPI** - Framework web asíncrono
- **SQLModel** - ORM (combina SQLAlchemy + Pydantic)
- **SQLite** (aiosqlite) - Base de datos asíncrona
- **NumPy** - Operaciones vectorizadas
- **Uvicorn** - Servidor ASGI

## Instalación

```bash
# Clonar el repositorio
git clone <url-del-repositorio>
cd example_server

# Crear entorno virtual
python -m venv env
source env/bin/activate  # Linux/Mac
# env\Scripts\activate   # Windows

# Instalar dependencias
pip install -r requirements.txt
```

## Uso

### Iniciar el servidor

```bash
python main.py
```

El servidor se levanta en `http://0.0.0.0:8000`.

La documentación interactiva (Swagger UI) está disponible en:

- Swagger: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Endpoint de prueba rápida

```bash
curl http://localhost:8000/docs
```

## Estructura del proyecto

```
example_server/
├── main.py                  # Punto de entrada de la aplicación
├── requirements.txt         # Dependencias
├── bulk.json                # Datos de prueba para bulk síncrono (inventario)
├── bulk_async.json          # Datos de prueba para bulk asíncrono (inventario)
└── src/
    ├── database/
    │   ├── __init__.py
    │   └── database.py      # Configuración de DB (SQLite async)
    ├── models/
    │   ├── __init__.py
    │   ├── users.py          # Modelo User
    │   ├── persons.py        # Modelo Person
    │   └── invectory.py      # Modelo Inventory
    ├── schemas/
    │   ├── __init__.py
    │   ├── user.py           # Schemas User (Create, Update, Response, BulkCreate)
    │   ├── persons.py        # Schemas Person
    │   └── inventory.py      # Schemas Inventory
    ├── routes/
    │   ├── __init__.py
    │   ├── user.py           # Endpoints de usuarios
    │   ├── persons.py        # Endpoints de personas
    │   └── inventory.py      # Endpoints de inventario
    ├── services/
    │   ├── user.py           # Lógica de negocio - usuarios
    │   ├── persons.py        # Lógica de negocio - personas
    │   └── inventory.py      # Lógica de negocio - inventario
    └── utils/
        └── utils.py
```

## Endpoints

### Usuarios (`/users`)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/users/` | Obtener todos los usuarios |
| POST | `/users/` | Crear un usuario |
| POST | `/users/bulk-numpy` | Crear usuarios usando NumPy (vectorizado) |
| POST | `/users/bulk-for` | Crear usuarios con un for secuencial |
| PUT | `/users/{user_id}` | Actualizar un usuario |
| DELETE | `/users/{user_id}` | Eliminar un usuario |

**Ejemplos:**

```bash
# Crear un usuario
curl -X POST http://localhost:8000/users/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Juan", "email": "juan@mail.com"}'

# Crear 1000 usuarios con NumPy (O(1) vectorizado)
curl -X POST http://localhost:8000/users/bulk-numpy \
  -H "Content-Type: application/json" \
  -d '{"quantity": 1000}'

# Crear 1000 usuarios con for secuencial (O(n))
curl -X POST http://localhost:8000/users/bulk-for \
  -H "Content-Type: application/json" \
  -d '{"quantity": 1000}'
```

### Inventario (`/inventory`)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/inventory/` | Obtener inventario filtrado y ordenado con `.sort()` (Timsort) |
| GET | `/inventory/all` | Obtener inventario ordenado delegando a la DB (SQL ORDER BY) |
| POST | `/inventory/` | Crear un item de inventario |
| POST | `/inventory/bulk` | Crear inventarios desde archivo JSON - inserción uno a uno (O(n)) |
| POST | `/inventory/bulck` | Crear inventarios desde archivo JSON - inserción bulk con `add_all` (O(1)) |
| PUT | `/inventory/{inventory_id}` | Actualizar un inventario |
| DELETE | `/inventory/{inventory_id}` | Eliminar un inventario |

**Ejemplos:**

```bash
# Crear un item de inventario
curl -X POST http://localhost:8000/inventory/ \
  -H "Content-Type: application/json" \
  -d '{"name": "producto_1", "amount": 100}'

# Insertar 100 items uno a uno (O(n))
curl -X POST http://localhost:8000/inventory/bulk \
  -H "Content-Type: application/json" \
  -d '{"quantity": 100}'

# Insertar 100 items con add_all (O(1))
curl -X POST http://localhost:8000/inventory/bulck \
  -H "Content-Type: application/json" \
  -d '{"quantity": 100}'
```

### Personas (`/persons`)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/persons/sorted` | Obtener personas ordenadas por edad (descendente) con `.sort()` |
| GET | `/persons/incremented-age` | Obtener personas con edad incrementada en 1 (iteración con for) |
| POST | `/persons/` | Crear una persona |
| PUT | `/persons/{person_id}` | Actualizar una persona |
| DELETE | `/persons/{person_id}` | Eliminar una persona |

**Ejemplos:**

```bash
# Crear una persona
curl -X POST http://localhost:8000/persons/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Ana", "passport": "AB123456", "age": 25}'
```

## Comparaciones de complejidad algorítmica

Este servidor permite comparar el rendimiento entre distintas implementaciones:

| Comparación | Endpoint A (lento) | Endpoint B (rápido) | Diferencia |
|-------------|-------------------|---------------------|------------|
| Creación bulk de usuarios | `POST /users/bulk-for` (O(n)) | `POST /users/bulk-numpy` (O(1) vectorizado) | For secuencial vs NumPy vectorizado |
| Creación bulk de inventario | `POST /inventory/bulk` (O(n)) | `POST /inventory/bulck` (O(1)) | Inserción individual vs `add_all` |
| Ordenamiento de inventario | `GET /inventory/` (Timsort en Python) | `GET /inventory/all` (SQL ORDER BY) | `.sort()` + `filter()` vs delegar a DB |
| Ordenamiento de personas | `GET /persons/sorted` | `GET /persons/incremented-age` | `.sort()` vs iteración con for |

Los endpoints que miden tiempo devuelven el campo `"time"` en la respuesta para facilitar comparaciones directas.

## Notas

- La base de datos SQLite se crea automáticamente al iniciar el servidor (`database.db`).
- Los archivos `bulk.json` y `bulk_async.json` contienen datos de prueba precargados para los endpoints de inventario bulk.
- Los modelos de la DB se crean automáticamente gracias al lifespan de FastAPI.