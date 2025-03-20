from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class UserBase(BaseModel):
    nombre: str
    primer_apellido: str
    segundo_apellido: str | None
    tipo_usuario: str
    nombre_usuario: str
    correo_electronico: str
    contrasena: str
    numero_telefono: str | None

    def normalize(self):
        self.tipo_usuario = self.tipo_usuario.upper()

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    pass

class User(UserBase):
    id: int
    fecha_registro: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None

    class Config:
        from_attributes = True

# Esquema para autenticación
class UserLogin(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    password: str
