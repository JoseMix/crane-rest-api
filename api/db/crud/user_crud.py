import json
import os
from sqlalchemy.orm import Session
from .. import models, schemas
from passlib.hash import pbkdf2_sha256
from api.config.constants import SECRET_KEY


def get_all(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email.strip()).first()


def register(db: Session, user: schemas.UserCreate):
    hashed_password = pbkdf2_sha256.hash(user.password, salt=SECRET_KEY)
    db_user = models.User(
        email=user.email,
        password=hashed_password,
        full_name=user.full_name,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def login(db: Session, user: schemas.UserLogin):
    db_user = get_by_email(db, user.email)
    if db_user:
        if pbkdf2_sha256.verify(user.password, db_user.password):
            return db_user
    return None


def add_user(db: Session, role_id: int, user_id: int):
    db_user_role = models.UserRole(
        role_id=role_id,
        user_id=user_id
    )
    db.add(db_user_role)
    db.commit()
    db.refresh(db_user_role)
    return db_user_role


def remove_user(db: Session, role_id: int, user_id: int):
    db_user_role = db.query(models.UserRole).filter(
        models.UserRole.role_id == role_id,
        models.UserRole.user_id == user_id
    ).first()
    if not db_user_role:
        return None

    db.delete(db_user_role)
    db.commit()
    return db_user_role
