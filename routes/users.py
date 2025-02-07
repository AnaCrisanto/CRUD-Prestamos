from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import crud.users
import config.db
import schemas.users
from typing import List

user = APIRouter()

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = config.db.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Obtener todos los usuarios
@user.get("/users", response_model=List[schemas.users.User], tags=["Usuarios"])
async def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    db_users = crud.users.get_users(db=db, skip=skip, limit=limit)
    return db_users

# Obtener un usuario por ID
@user.get("/users/{id}", response_model=schemas.users.User, tags=["Usuarios"])
async def read_user(id: int, db: Session = Depends(get_db)):
    db_user = crud.users.get_user(db=db, id=id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Crear un nuevo usuario
@user.post("/users", response_model=schemas.users.User, tags=["Usuarios"])
async def create_user(user_data: schemas.users.UserCreate, db: Session = Depends(get_db)):
    return crud.users.create_user(db=db, user=user_data)

# Actualizar un usuario existente
@user.put("/users/{id}", response_model=schemas.users.User, tags=["Usuarios"])
async def update_user(id: int, user_data: schemas.users.UserUpdate, db: Session = Depends(get_db)):
    db_user = crud.users.update_user(db=db, id=id, user_data=user_data)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Eliminar un usuario
@user.delete("/users/{id}", response_model=dict, tags=["Usuarios"])
async def delete_user(id: int, db: Session = Depends(get_db)):
    result = crud.users.delete_user(db=db, id=id)
    if result is None:
        raise HTTPException(status_code=404, detail="User not found")
    return result
