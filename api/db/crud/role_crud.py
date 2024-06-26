from sqlalchemy.orm import Session
from api.db import models, schemas


def get_all(db: Session, skip: int = 0, limit: int = 100):
    ''' Get all roles '''
    return db.query(models.Role).offset(skip).limit(limit).all()


def get_by_id(db: Session, role_id: int):
    ''' Get role by ID '''
    return db.query(models.Role).filter(models.Role.id == role_id).first()


def get_by_name(db: Session, name: str):
    ''' Get role by name '''
    return db.query(models.Role).filter(models.Role.name == name).first()


def create(db: Session, role: schemas.RoleCreate):
    ''' Create a new role '''
    db_role = models.Role(**role.dict())
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role


def update(db: Session, role_id: int, role: schemas.RoleUpdate):
    ''' Update a role '''
    db_role = db.query(models.Role).filter(
        models.Role.id == role_id).first()
    if not db_role:
        return None

    for key, value in role.dict().items():
        setattr(db_role, key, value)

    db.commit()
    db.refresh(db_role)
    return db_role


def delete(db: Session, role_id: int):
    ''' Delete a role '''
    db_role = db.query(models.Role).filter(
        models.Role.id == role_id).first()
    if not db_role:
        return None

    db.delete(db_role)
    db.commit()
    return db_role


def create_for_user(db: Session, user_id: int, role_id: int):
    ''' Create a new role for a user '''
    db_user_role = models.UserRole(user_id=user_id, role_id=role_id)
    db.add(db_user_role)
    db.commit()
    db.refresh(db_user_role)
    return db_user_role


def remove_user(db: Session, user_id: int, role_id: int):
    ''' Remove a role from a user '''
    db_user_role = db.query(models.UserRole).filter(
        models.UserRole.role_id == role_id,
        models.UserRole.user_id == user_id
    ).first()
    if not db_user_role:
        return None

    db.delete(db_user_role)
    db.commit()
    return db_user_role


def get_roles_by_user(db: Session, db_user: models.User):
    ''' Get roles by user '''
    return db.query(models.Role).join(models.UserRole).filter(models.UserRole.user_id == db_user.id).all()
