import json
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from api.db import models, schemas


def get_by_name(db: Session, name: str, user_id: int = None):
    ''' Get app by name '''
    return db.query(models.App).filter(and_(models.App.name == name, models.App.deleted_at == None)).filter(or_(models.App.user_id == user_id, user_id is None)).first()


def get_by_id(db: Session, app_id: int, user_id: int = None):
    ''' Get app by id '''
    return db.query(models.App).filter(and_(models.App.id == app_id, models.App.deleted_at == None)).filter(or_(models.App.user_id == user_id, user_id is None)).first()


def get_all(db: Session, user_id: int = None, skip: int = 0, limit: int = 100):
    ''' Get all apps '''
    return db.query(models.App).filter(models.App.deleted_at == None).filter(or_(models.App.user_id == user_id, user_id is None)).offset(skip).limit(limit).all()


def create(db: Session, user_app: schemas.AppCreate):
    ''' Create app '''
    app_dict = user_app.dict()
    app_dict["services"] = json.dumps(app_dict["services"])
    db_app = models.App(**app_dict)

    db.add(db_app)
    db.commit()
    db.refresh(db_app)
    return db_app


def update(db: Session, app: schemas.App):
    ''' Update app '''
    app.services = json.dumps(app.services)
    app.hosts = json.dumps(app.hosts)

    db.commit()
    db.refresh(app)
    return app


def delete_logical(db: Session, app_id: str, user_id: int = None):
    ''' Logical delete app '''
    db_app = get_by_id(db, app_id, user_id)
    db_app.deleted_at = datetime.now()
    db.commit()
    return db_app


def delete_physical(db: Session, app_id: str, user_id: int = None):
    ''' Physical delete app '''
    db_app = get_by_name(db, app_id, user_id)
    db.delete(db_app)
    db.commit()
    return db_app
