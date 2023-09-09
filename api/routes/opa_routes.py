from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from api.db.database import get_db
import api.db.crud.opa_crud as OPAConfigRepository
from api.db.schemas import OPAConfigCreate, OPAConfigUpdate, OPAConfigInDB
from api.clients.OPAClient import test, get_policies, update_policies_file
opaConfigRouter = APIRouter()


@opaConfigRouter.post("/", response_model=OPAConfigInDB)
def create(opa_config: OPAConfigCreate, db: Session = Depends(get_db)):
    return OPAConfigRepository.create_opa_config(db=db, opa_config=opa_config)


@opaConfigRouter.post("/test", response_model=OPAConfigInDB)
def testHelper(opa_config: OPAConfigCreate, db: Session = Depends(get_db)):
    return test(db, opa_config)

@opaConfigRouter.get("/testDB")
def testDB(db: Session = Depends(get_db)):
    return update_policies_file(db)


@opaConfigRouter.get("/", response_model=List[OPAConfigInDB])
def get_all(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return OPAConfigRepository.get_all(db=db, skip=skip, limit=limit)


@opaConfigRouter.get("/policies", response_model=List[str])
def get_policies_list():
    return get_policies()


@opaConfigRouter.get("/{opa_config_id}", response_model=OPAConfigInDB)
def get_by_id(opa_config_id: int, db: Session = Depends(get_db)):
    opa_config = OPAConfigRepository.get_by_id(db, opa_config_id)
    if not opa_config:
        raise HTTPException(status_code=404, detail="OPAConfig not found")
    return opa_config


@opaConfigRouter.put("/{opa_config_id}", response_model=OPAConfigInDB)
def update(opa_config_id: int, opa_config: OPAConfigUpdate, db: Session = Depends(get_db)):
    updated_opa_config = OPAConfigRepository.update(
        db, opa_config_id, opa_config)
    if not updated_opa_config:
        raise HTTPException(status_code=404, detail="OPAConfig not found")
    return updated_opa_config


@opaConfigRouter.delete("/{opa_config_id}", response_model=OPAConfigInDB)
def delete(opa_config_id: int, db: Session = Depends(get_db)):
    deleted_opa_config = OPAConfigRepository.delete(
        db, opa_config_id)
    if not deleted_opa_config:
        raise HTTPException(status_code=404, detail="OPAConfig not found")
    return deleted_opa_config
