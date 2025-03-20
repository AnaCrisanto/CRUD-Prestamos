from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.users import user_router as user
from routes.loans import loan
from routes.materials import material
from config.db import engine, Base

# Inicializar la aplicación FastAPI
app = FastAPI(
    title="PRESTAMOS S.A. de C.V.",
    description="API de prueba para almacenar registros de préstamo de material educativo",
    docs_url="/docs",  # URL personalizada para la documentación interactiva
    redoc_url="/redoc",  # URL personalizada para la documentación con Redoc
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},  # Deshabilitar OAuth2 en Swagger UI
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://prestamosana.netlify.app"],  # Permite tu frontend en Vue
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos HTTP
    allow_headers=["*"],  # Permite todos los headers
)

# Crear las tablas en la base de datos (si no existen)
Base.metadata.create_all(bind=engine)

# Incluir las rutas de la API
app.include_router(user)
app.include_router(loan)
app.include_router(material)

@app.get("/", tags=["Bienvenida"])
def read_root():
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
