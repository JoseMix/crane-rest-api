import json
from datetime import datetime
from sqlalchemy.orm import Session
from .. import models, schemas
from passlib.hash import pbkdf2_sha256
from api.config.constants import SECRET_KEY


def get_by_name(db: Session, db_user: models.User, name: str):
    return db.query(models.App).filter(models.App.name == name.strip()).filter(models.App.user_id == db_user.id).first()


def get_by_id(db: Session, db_user: models.User, id: int):
    return db.query(models.App).filter(models.App.id == id).filter(models.App.user_id == db_user.id).first()


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


def update(db: Session, db_user, app_id: str, app: schemas.App):
    db_app = get_by_id(db, db_user, app_id)
    update_data = app.dict(exclude_unset=True)
    update_data["services"] = json.dumps(update_data["services"])
    update_data["ports"] = json.dumps(update_data["ports"])
    update_data["hosts"] = json.dumps(update_data["hosts"])
    for key, value in update_data.items():
        setattr(db_app, key, value)
    db.commit()
    db.refresh(db_app)
    return db_app


def delete_logical(db: Session, db_user, app_id: str,):
    db_app = get_by_id(db, db_user, app_id)
    db_app.deleted_at = datetime.now()
    db.commit()
    return db_app


def delete_physical(db: Session, db_user, app_id: str,):
    db_app = get_by_name(db, db_user, app_id)
    db.delete(db_app)
    db.commit()
    return db_app
