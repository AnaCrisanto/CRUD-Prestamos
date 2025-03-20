from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from datetime import timedelta
from config.db import get_db
from schemas.users import UserLogin, User, UserCreate, UserUpdate
from crud.users import authenticate_user, get_users, get_user, create_user, update_user, delete_user  # Importa las funciones necesarias
from config.jwt import create_access_token, get_current_user

user_router = APIRouter()
security = HTTPBearer()

# Endpoint de autenticación
@user_router.post("/login", response_model=dict, tags=["Autenticación"])
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    authenticated_user = authenticate_user(db, username=user_data.username, email=user_data.email, phone=user_data.phone, password=user_data.password)
    if not authenticated_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(data={"sub": authenticated_user.nombre_usuario}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}

# Ruta protegida
@user_router.get("/protected", response_model=User, tags=["Autenticación"])
async def protected_route(current_user: User = Depends(get_current_user)):
    return current_user

# Obtener todos los usuarios (protegido)
@user_router.get("/users", response_model=list[User], tags=["Usuarios"])
async def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_users = get_users(db=db, skip=skip, limit=limit)  # Usa la función importada directamente
    return db_users

# Obtener un usuario por ID (protegido)
@user_router.get("/users/{id}", response_model=User, tags=["Usuarios"])
async def read_user(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_user = get_user(db=db, id=id)  # Usa la función importada directamente
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Crear un nuevo usuario (desprotegido)
@user_router.post("/users", response_model=User, tags=["Usuarios"])
async def create_new_user(user_data: UserCreate, db: Session = Depends(get_db)):
    return create_user(db=db, user=user_data)  # Llama a la función del módulo crud.users

# Actualizar un usuario existente (protegido)
@user_router.put("/users/{id}", response_model=User, tags=["Usuarios"])
async def update_existing_user(id: int, user_data: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_user = update_user(db=db, id=id, user_data=user_data)  # Usa la función importada directamente
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Eliminar un usuario (protegido)
@user_router.delete("/users/{id}", response_model=dict, tags=["Usuarios"])
async def delete_existing_user(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = delete_user(db=db, id=id)  # Usa la función importada directamente
    if result is None:
        raise HTTPException(status_code=404, detail="User not found")
    return result
