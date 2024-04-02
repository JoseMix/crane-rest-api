import json
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from api.db import models, schemas
from passlib.hash import pbkdf2_sha256
from api.config.constants import SECRET_KEY


def get_by_name(db: Session, name: str, user_id: int = None):
    return db.query(models.App).filter(and_(models.App.name == name, models.App.deleted_at == None)).filter(or_(models.App.user_id == user_id, user_id is None)).first()


def get_by_id(db: Session, id: int, user_id: int = None):
    return db.query(models.App).filter(and_(models.App.id == id, models.App.deleted_at == None)).filter(or_(models.App.user_id == user_id, user_id is None)).first()


def get_all(db: Session, user_id: int = None, skip: int = 0, limit: int = 100):
    return db.query(models.App).filter(or_(models.App.user_id == user_id, user_id is None)).filter(models.App.deleted_at == None).offset(skip).limit(limit).all()


def create(db: Session, userApp: schemas.AppCreate):
    app_dict = userApp.dict()
    app_dict["services"] = json.dumps(app_dict["services"])
    db_app = models.App(**app_dict)

    db.add(db_app)
    db.commit()
    db.refresh(db_app)
    return db_app


def update(db: Session, app_id: str, app: schemas.App, user_id: int = None):
    db_app = get_by_id(db, app_id, user_id)
    update_data = app.dict(exclude_unset=True)
    update_data["services"] = json.dumps(update_data["services"])
    update_data["ports"] = json.dumps(update_data["ports"])
    update_data["hosts"] = json.dumps(update_data["hosts"])
    for key, value in update_data.items():
        setattr(db_app, key, value)
    db.commit()
    db.refresh(db_app)
    return db_app


def delete_logical(db: Session, app_id: str, user_id: int = None):
    db_app = get_by_id(db, app_id, user_id)
    db_app.deleted_at = datetime.now()
    db.commit()
    return db_app


def delete_physical(db: Session, app_id: str, user_id: int = None):
    db_app = get_by_name(db, app_id, user_id)
    db.delete(db_app)
    db.commit()
    return db_app
