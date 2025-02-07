"""
Módulo db.py

Este módulo configura la conexión a la base de datos utilizando SQLAlchemy.
Define el motor de la base de datos, la sesión local y la clase base para los modelos.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de conexión a la base de datos MySQL
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:220138@localhost:3306/base_prueba"

# Crear el motor de la base de datos
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Crear una fábrica de sesiones locales
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase base para los modelos SQLAlchemy
Base = declarative_base()
