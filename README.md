# Proyecto E-commerce API (FastAPI + SQLAlchemy 2.0)

Esta API ha sido construida como base moderna utilizando **FastAPI** y **SQLAlchemy 2.0**.

## 🚀 Cómo usar y ejecutar este código

### 1. Requisitos Previos
- Python instalado en tu sistema.
- Servidor PostgreSQL corriendo en el puerto `5433` (según `app/db.py`).
- Entorno virtual (venv) activado.

### 2. Ejecutar el Servidor
Para arrancar el programa y levantar el servidor local en modo desarrollo, corre este comando en tu terminal (asegúrate de estar en la carpeta raíz del proyecto):

```bash
uvicorn app.main:app --reload
```

El servidor estará accesible en: `http://localhost:8000`

### 3. Explorar y Probar Endpoints Interactivos (Swagger UI)
FastAPI genera documentación interactiva automáticamente. Simplemente ve a tu navegador e ingresa a:
- [http://localhost:8000/docs](http://localhost:8000/docs)

Desde allí puedes probar la API haciendo clic en "Try it out".

### 4. Crear un Usuario (Ruta POST /users)
Para registrar un usuario mediante cURL o postman, envía una solicitud `POST` a `http://localhost:8000/users` con el siguiente cuerpo en JSON:

```json
{
  "email": "test@correo.com",
  "password": "mi_password_seguro",
  "first_name": "Juan",
  "last_name": "Pérez"
}
```

Al utilizar `password` en el body, la API encriptará y depositará un hash dentro de la columna `password_hash` en PostgreSQL de manera segura.

---

## 📚 Guía Técnica: SQLAlchemy 2.0, FastAPI y Pydantic

El proyecto ha sido actualizado a la versión moderna **2.0** de SQLAlchemy. 

### 1. Modelos (`models.py`)
En la versión **2.0**, los modelos se enfocan firmemente en el análisis de tipos nativo usando la sintaxis `Mapped` y `mapped_column`.

```python
from sqlalchemy import String, Uuid, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import uuid
from datetime import datetime, timezone

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    
    # Manejo de Fechas correctas
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc)
    )
```

### 2. Pydantic y Schemas (`schemas.py`)
Tu `schemas.py` dicta cómo deben verse los JSON que entran o salen. La clave aquí es `from_attributes = True`, esto indica a Pydantic que formatee los objetos de base de datos obtenidos por SQLAlchemy a JSON dicts de manera automática:

```python
class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    is_active: bool

    class Config:
        from_attributes = True
```

### 3. Endpoints y Consultas 2.0 (`main.py`)
Ya no se usa `db.query()`. Se separan fuertemente los Statements (consultas preparadas) de la Ejecución propia. Ahora usamos el motor con `db.execute(select(...))`.

**Traer Todos:**
```python
# ❌ Antiguo (SQLA 1.4): db.query(User).filter(...).all()
# ✅ Moderno (SQLA 2.0):
stmt = select(User).where(User.deleted_at.is_(None))
users = db.execute(stmt).scalars().all()
```

**Traer Solo Uno (`.first()`):**
```python
stmt = select(User).where(User.email == "test@correo.com")
user = db.execute(stmt).scalars().first()
```

### ¿Por qué cambiamos validaciones nativas de Fechas?
Un error común sucede cuando PostgreSQL no tiene valores `DEFAULT CURRENT_TIMESTAMP` en las columnas. Si definíamos `server_default`, la base de datos se quejaba. 
Es por eso que en el código de tu E-commerce utilizamos `default=lambda: datetime.now(timezone.utc)`. Al usar solo `default`, instruimos a la app de que **Python asigne la fecha** en vez de tirarle todo el trabajo al motor SQL, resolviendo permanentemente problemas de dependencias en columnas Not-Null (constraints).
