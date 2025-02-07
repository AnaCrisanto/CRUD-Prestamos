"""
Módulo principal de la aplicación FastAPI.

Este archivo inicializa la aplicación FastAPI, configura las rutas y crea las tablas en la
base de datos si no existen.
"""

from fastapi import FastAPI
from routes.users import user
from routes.loans import loan
from routes.materials import material
from config.db import engine, Base  # Importa el motor y Base

# Inicializar la aplicación FastAPI
app = FastAPI(
    title="PRESTAMOS S.A. de C.V.",
    description="API de prueba para almacenar registros de préstamo de material educativo",
    docs_url="/docs",  # URL personalizada para la documentación interactiva
    redoc_url="/redoc",  # URL personalizada para la documentación con Redoc
)

# Crear las tablas en la base de datos (si no existen)
Base.metadata.create_all(bind=engine)

# Incluir las rutas de la API
app.include_router(user)
app.include_router(loan)
app.include_router(material)


@app.get("/", tags=["Bienvenida"])
def read_root():
    """
    Ruta raíz de la API.

    Devuelve un mensaje de bienvenida y una lista de rutas disponibles.
    """
    return {
        "message": "Bienvenido a la API de PRESTAMOS S.A. de C.V.",
        "docs": "Visita '/docs' para la documentación interactiva de la API.",
        "redoc": "Visita '/redoc' para la documentación con Redoc.",
        "available_routes": [
            "/users (GET) - Lista de usuarios",
            "/users/{user_id} (GET) - Obtener detalles de un usuario",
            "/users (POST) - Crear un nuevo usuario",
            "/loans (GET) - Lista de préstamos",
            "/loans/{loan_id} (GET) - Obtener detalles de un préstamo",
            "/loans (POST) - Crear un nuevo préstamo",
            "/materials (GET) - Lista de materiales",
            "/materials/{material_id} (GET) - Obtener detalles de un material",
            "/materials (POST) - Crear un nuevo material",
        ],
    }
