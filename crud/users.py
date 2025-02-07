import models.users
import schemas.users
from sqlalchemy.orm import Session

# Obtener todos los usuarios
def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.users.User).offset(skip).limit(limit).all()

# Obtener un usuario por ID
def get_user(db: Session, id: int):
    return db.query(models.users.User).filter(models.users.User.id == id).first()

# Crear un nuevo usuario
def create_user(db: Session, user: schemas.users.UserCreate):
    db_user = models.users.User(
        nombre=user.nombre,
        primer_apellido=user.primer_apellido,
        segundo_apellido=user.segundo_apellido,
        tipo_usuario=user.tipo_usuario,
        nombre_usuario=user.nombre_usuario,
        correo_electronico=user.correo_electronico,
        contrasena=user.contrasena,
        numero_telefono=user.numero_telefono,
        estatus=user.estatus,
        # No se pasa fecha_registro ni fecha_actualizacion, ya que son automáticas
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Actualizar un usuario existente
def update_user(db: Session, id: int, user_data: schemas.users.UserUpdate):
    db_user = db.query(models.users.User).filter(models.users.User.id == id).first()
    if db_user is None:
        return None  # Usuario no encontrado

    # Actualizar los campos del usuario
    db_user.nombre = user_data.nombre
    db_user.primer_apellido = user_data.primer_apellido
    db_user.segundo_apellido = user_data.segundo_apellido
    db_user.tipo_usuario = user_data.tipo_usuario
    db_user.nombre_usuario = user_data.nombre_usuario
    db_user.correo_electronico = user_data.correo_electronico
    db_user.contrasena = user_data.contrasena
    db_user.numero_telefono = user_data.numero_telefono
    db_user.estatus = user_data.estatus
    # fecha_actualizacion se actualiza automáticamente gracias a `onupdate` en el modelo

    db.commit()
    db.refresh(db_user)
    return db_user

# Eliminar un usuario
def delete_user(db: Session, id: int):
    db_user = db.query(models.users.User).filter(models.users.User.id == id).first()
    if db_user is None:
        return None  # Usuario no encontrado

    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}
