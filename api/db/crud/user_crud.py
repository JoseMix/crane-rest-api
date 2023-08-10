import json
import os
from sqlalchemy.orm import Session
from .. import models, schemas
from passlib.hash import pbkdf2_sha256


SECRET_KEY = os.getenv("SECRET_KEY")


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
        is_active=user.is_active,
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
