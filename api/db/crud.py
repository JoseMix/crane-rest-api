import json
import os
from sqlalchemy.orm import Session
from . import models, schemas
from passlib.hash import pbkdf2_sha256

SECRET_KEY = os.getenv("SECRET_KEY")


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
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


def get_service_by_name_and_user(db: Session, name: str, db_user: models.User):
    return db.query(models.Service).filter(models.Service.name == name).filter(models.Service.user_id == db_user.id).first()


def get_services(db: Session, db_user: models.User, skip: int = 0, limit: int = 100):
    return db.query(models.Service).filter(models.Service.user_id == db_user.id).offset(skip).limit(limit).all()


def create_user_app(db: Session, userApp: schemas.ServiceCreate, db_user):
    service_dict = userApp.dict()
    service_dict["services"] = json.dumps(service_dict["services"])
    db_service = models.Service(**service_dict)

    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service


def login_user(db: Session, user: schemas.UserLogin):
    db_user = get_user_by_email(db, user.email)
    if db_user:
        if pbkdf2_sha256.verify(user.password, db_user.password):
            return db_user
    return None
