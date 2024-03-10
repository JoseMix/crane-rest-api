from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from api.db.database import get_db
from api.db.crud.role_crud import get_all, get_by_id, create, update, delete, create_for_user, remove_user, get_roles_by_user
from api.db.schemas import RoleCreate, RoleUpdate, Role
from api.services.role_service import verify
from api.routes.auth_routes import verify_jwt

roleRouter = APIRouter()


@roleRouter.get("/verify")
async def verify_user_role(db_user=Depends(verify_jwt), db: Session = Depends(get_db)):
    result = await verify(db, db_user, "ROLES", "GET")
    return result


@roleRouter.get("/", response_model=List[Role])
def get_all_roles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_all(db=db, skip=skip, limit=limit)


@roleRouter.get("/{role_id}", response_model=Role)
def get_role_by_id(role_id: int, db: Session = Depends(get_db)):
    role = get_by_id(db, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role


@roleRouter.post("/", response_model=Role)
def create_role(role: RoleCreate, db: Session = Depends(get_db)):
    return create(db=db, role=role)


@roleRouter.put("/{role_id}", response_model=Role)
def update_role(role_id: int, role: RoleUpdate, db: Session = Depends(get_db)):
    updated_role = update(db, role_id, role)
    if not updated_role:
        raise HTTPException(status_code=404, detail="Role not found")
    return updated_role


@roleRouter.delete("/{role_id}", response_model=Role)
def delete_role(role_id: int, db: Session = Depends(get_db)):
    deleted_role = delete(db, role_id)
    if not deleted_role:
        raise HTTPException(status_code=404, detail="Role not found")
    return deleted_role


@roleRouter.post("/{role_id}/user/{user_id}")
def create_role_for_user(user_id: int, role_id: int, db: Session = Depends(get_db)):
    return create_for_user(db, user_id, role_id)


@roleRouter.delete("/{role_id}/user/{user_id}")
def remove_role_from_user(user_id: int, role_id: int, db: Session = Depends(get_db)):
    return remove_user(db, user_id, role_id)


@roleRouter.get("/user/{user_id}")
def get_user_roles(user_id: int, db: Session = Depends(get_db)):
    return get_roles_by_user(db, user_id)
