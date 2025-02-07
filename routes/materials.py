from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import crud.materials
import config.db
import schemas.materials
from typing import List

# Crear un router para los materiales
material = APIRouter()

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = config.db.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Obtener todos los materiales
@material.get("/materials", response_model=List[schemas.materials.Material], tags=["Materiales"])
async def read_materials(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Obtiene una lista de materiales con paginación.
    """
    db_materials = crud.materials.get_materials(db=db, skip=skip, limit=limit)
    return db_materials

# Obtener un material por ID
@material.get("/materials/{id}", response_model=schemas.materials.Material, tags=["Materiales"])
async def read_material(id: int, db: Session = Depends(get_db)):
    """
    Obtiene un material por su ID.
    """
    db_material = crud.materials.get_material(db=db, id=id)
    if db_material is None:
        raise HTTPException(status_code=404, detail="Material not found")
    return db_material

# Crear un nuevo material
@material.post("/materials", response_model=schemas.materials.Material, tags=["Materiales"])
async def create_material(material_data: schemas.materials.MaterialCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo material.
    """
    return crud.materials.create_material(db=db, material=material_data)

# Actualizar un material existente
@material.put("/materials/{id}", response_model=schemas.materials.Material, tags=["Materiales"])
async def update_material(id: int, material_data: schemas.materials.MaterialUpdate, db: Session = Depends(get_db)):
    """
    Actualiza un material existente.
    """
    db_material = crud.materials.update_material(db=db, id=id, material_data=material_data)
    if db_material is None:
        raise HTTPException(status_code=404, detail="Material not found")
    return db_material

# Eliminar un material
@material.delete("/materials/{id}", response_model=dict, tags=["Materiales"])
async def delete_material(id: int, db: Session = Depends(get_db)):
    """
    Elimina un material por su ID.
    """
    result = crud.materials.delete_material(db=db, id=id)
    if result is None:
        raise HTTPException(status_code=404, detail="Material not found")
    return result
