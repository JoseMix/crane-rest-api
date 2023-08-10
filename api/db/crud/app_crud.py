import json
import os
from datetime import datetime
from sqlalchemy.orm import Session
from .. import models, schemas
from passlib.hash import pbkdf2_sha256

SECRET_KEY = os.getenv("SECRET_KEY")


def get_by_name(db: Session, name: str, db_user: models.User):
    return db.query(models.App).filter(models.App.name == name.strip()).filter(models.App.user_id == db_user.id).first()


def get_all(db: Session, db_user: models.User, skip: int = 0, limit: int = 100):
    return db.query(models.App).filter(models.App.user_id == db_user.id).offset(skip).limit(limit).all()


def create(db: Session, userApp: schemas.AppCreate):
    app_dict = userApp.dict()
    app_dict["services"] = json.dumps(app_dict["services"])
    db_app = models.App(**app_dict)

    db.add(db_app)
    db.commit()
    db.refresh(db_app)
    return db_app


def update(db: Session, db_user, app_name, app: schemas.ServiceUpdate):
    db_app = get_by_name(db, app_name, db_user)
    db_app.apps = json.dumps(app.apps)
    db.commit()
    db.refresh(db_app)
    return db_app

def delete_logical(db: Session, db_user, app_name):
    db_app = get_by_name(db, app_name, db_user)
    db_app.deleted_at = datetime.now()
    db.commit()
    return db_app
