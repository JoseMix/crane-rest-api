from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from api.db.database import get_db
import api.db.crud.opa_crud as OPAConfigRepository
from api.db.schemas import OPAConfigCreate, OPAConfigUpdate, OPAConfigInDB, OPAPolicyCheck, OPAPolicyCreate, OPAPolicyCreateData
from api.clients.OPAClient import test, get_policies, update_policies_file, delete_opa_policy, check_policy, create_opa_policy, update_or_create_opa_data
opaConfigRouter = APIRouter()

# ENDPOINTS QUE ESCRIBEN EN LA BASE DE DATOS


@opaConfigRouter.get("/configs", response_model=List[OPAConfigInDB])
def get_all_configs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return OPAConfigRepository.get_all(db=db, skip=skip, limit=limit)


@opaConfigRouter.get("/configs/{opa_config_id}", response_model=OPAConfigInDB)
def get_config_by_id(opa_config_id: int, db: Session = Depends(get_db)):
    opa_config = OPAConfigRepository.get_by_id(db, opa_config_id)
    if not opa_config:
        raise HTTPException(status_code=404, detail="OPAConfig not found")
    return opa_config


@opaConfigRouter.post("/configs", response_model=OPAConfigInDB)
def create_config(opa_config: OPAConfigCreate, db: Session = Depends(get_db)):
    return OPAConfigRepository.create(db=db, opa_config=opa_config)


@opaConfigRouter.put("/configs/{opa_config_id}", response_model=OPAConfigInDB)
def update_config(opa_config_id: int, opa_config: OPAConfigUpdate, db: Session = Depends(get_db)):
    updated_opa_config = OPAConfigRepository.update(
        db, opa_config_id, opa_config)
    if not updated_opa_config:
        raise HTTPException(status_code=404, detail="OPAConfig not found")
    return updated_opa_config


@opaConfigRouter.delete("/configs/{opa_config_id}", response_model=OPAConfigInDB)
def delete_config(opa_config_id: int, db: Session = Depends(get_db)):
    deleted_opa_config = OPAConfigRepository.delete(
        db, opa_config_id)
    if not deleted_opa_config:
        raise HTTPException(status_code=404, detail="OPAConfig not found")
    return deleted_opa_config

# ENDPOINTS QUE ESCRIBEN EN OPA


@opaConfigRouter.post("/policies", response_model=bool)
def create_policy(opa_config: OPAPolicyCreate):
    return create_opa_policy(opa_config.policy_content, opa_config.policy_name)


@opaConfigRouter.post("/data", response_model=bool)
def create_data(opa_config: OPAPolicyCreateData):
    return update_or_create_opa_data(opa_config.data, opa_config.name)


@opaConfigRouter.delete("/policies/{policy_name}", response_model=bool)
def delete_policy(policy_name: str):
    if policy_name not in get_policies():
        raise HTTPException(status_code=404, detail="Policy not found")
    return delete_opa_policy(policy_name)


@opaConfigRouter.post("/policies/check")
def check_policies(opa_policy_check: OPAPolicyCheck):
    if opa_policy_check.policy_name not in get_policies():
        raise HTTPException(status_code=404, detail="Policy not found")
    return check_policy(opa_policy_check.policy_name, opa_policy_check.rule_name, opa_policy_check.input_data)


@opaConfigRouter.post("/test", response_model=OPAConfigInDB)
def testHelper(opa_config: OPAConfigCreate, db: Session = Depends(get_db)):
    return test(db, opa_config)


@opaConfigRouter.post("/testDB")
def testDB(db: Session = Depends(get_db)):
    return update_policies_file(db)


@opaConfigRouter.get("/policies", response_model=List[str])
def get_policies_list():
    return get_policies()
