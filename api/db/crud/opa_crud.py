from sqlalchemy.orm import Session
from .. import models, schemas


def get_all(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.OPAConfig).offset(skip).limit(limit).all()


def get_by_id(db: Session, opa_config_id: int):
    return db.query(models.OPAConfig).filter(models.OPAConfig.id == opa_config_id).first()


def get_by_name(db: Session, opa_config_name: str):
    return db.query(models.OPAConfig).filter(models.OPAConfig.name == opa_config_name).first()


def create(db: Session, opa_config: schemas.OPAConfigCreate):
    db_opa_config = models.OPAConfig(**opa_config.dict())
    db.add(db_opa_config)
    db.commit()
    db.refresh(db_opa_config)
    return db_opa_config


def update(db: Session, opa_config_id: int, opa_config: schemas.OPAConfigUpdate):
    db_opa_config = db.query(models.OPAConfig).filter(
        models.OPAConfig.id == opa_config_id).first()
    if not db_opa_config:
        return None

    for key, value in opa_config.dict().items():
        setattr(db_opa_config, key, value)

    db.commit()
    db.refresh(db_opa_config)
    return db_opa_config


def delete(db: Session, opa_config_id: int):
    db_opa_config = db.query(models.OPAConfig).filter(
        models.OPAConfig.id == opa_config_id).first()
    if not db_opa_config:
        return None

    db.delete(db_opa_config)
    db.commit()
    return db_opa_config
