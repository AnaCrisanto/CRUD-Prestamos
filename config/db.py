from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener la URL de conexión desde las variables de entorno
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Crear el motor de la base de datos con los parámetros SSL adecuados
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={
        "ssl": {
            "ssl_ca": "path_to_ca_certificate.pem",  # Asegúrate de poner la ruta del certificado CA
            "ssl_cert": "path_to_client_cert.pem",    # Si es necesario, pon la ruta del certificado del cliente
            "ssl_key": "path_to_client_key.pem",      # Si es necesario, pon la ruta de la clave del cliente
        }
    }
)

# Crear una fábrica de sesiones locales
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase base para los modelos SQLAlchemy
Base = declarative_base()

# Función para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
