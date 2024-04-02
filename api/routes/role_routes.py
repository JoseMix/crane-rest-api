''' This module contains the routes for the Role model. '''
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.db.database import get_db
from api.db.crud.role_crud import get_all, get_by_id, create, update, delete, create_for_user, remove_user, get_roles_by_user
from api.db.schemas import RoleCreate, RoleUpdate, Role
from api.routes.auth_routes import verify_jwt


roleRouter = APIRouter()


@roleRouter.get("/", response_model=List[Role], dependencies=[Depends(verify_jwt)])
def get_all_roles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    ''' Get all roles '''
    return get_all(db=db, skip=skip, limit=limit)


@roleRouter.get("/{role_id}", response_model=Role, dependencies=[Depends(verify_jwt)])
def get_role_by_id(role_id: int, db: Session = Depends(get_db)):
    ''' Get role by id '''
    role = get_by_id(db, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role


@roleRouter.post("/", response_model=Role, dependencies=[Depends(verify_jwt)])
def create_role(role: RoleCreate, db: Session = Depends(get_db)):
    ''' Create a new role '''
    return create(db=db, role=role)


@roleRouter.put("/{role_id}", response_model=Role, dependencies=[Depends(verify_jwt)])
def update_role(role_id: int, role: RoleUpdate, db: Session = Depends(get_db)):
    ''' Update a role '''
    updated_role = update(db, role_id, role)
    if not updated_role:
        raise HTTPException(status_code=404, detail="Role not found")
    return updated_role


@roleRouter.delete("/{role_id}", response_model=Role, dependencies=[Depends(verify_jwt)])
def delete_role(role_id: int, db: Session = Depends(get_db)):
    ''' Delete a role '''
    deleted_role = delete(db, role_id)
    if not deleted_role:
        raise HTTPException(status_code=404, detail="Role not found")
    return deleted_role


@roleRouter.post("/{role_id}/user/{user_id}", response_model=Role, dependencies=[Depends(verify_jwt)])
def create_role_for_user(user_id: int, role_id: int, db: Session = Depends(get_db)):
    ''' Create a role for a user '''
    return create_for_user(db, user_id, role_id)


@roleRouter.delete("/{role_id}/user/{user_id}", response_model=Role, dependencies=[Depends(verify_jwt)])
def remove_role_from_user(user_id: int, role_id: int, db: Session = Depends(get_db)):
    ''' Remove a role from a user '''
    return remove_user(db, user_id, role_id)


@roleRouter.get("/user/{user_id}", response_model=List[Role], dependencies=[Depends(verify_jwt)])
def get_user_roles(user_id: int,  db: Session = Depends(get_db)):
    ''' Get all roles for a user '''
    return get_roles_by_user(db, user_id)
