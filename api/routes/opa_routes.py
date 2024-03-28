from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from api.db.database import get_db
from api.routes.auth_routes import verify_jwt
from api.db.schemas import OPAConfigCreate, OPAPolicyCheck, OPAPolicyCreate, OPAPolicyCreateData
from api.clients.OPAClient import get_policies, delete_opa_policy, check_policy, create_opa_policy, update_or_create_opa_data
opaConfigRouter = APIRouter()


@opaConfigRouter.get("/policies", response_model=List[str])
def get_policies_list(db_user=Depends(verify_jwt)):
    return get_policies()


@opaConfigRouter.post("/policies", response_model=bool)
def create_policy(opa_config: OPAPolicyCreate, db_user=Depends(verify_jwt)):
    return create_opa_policy(opa_config.policy_content, opa_config.policy_name)


@opaConfigRouter.post("/data", response_model=bool)
def create_data(opa_config: OPAPolicyCreateData, db_user=Depends(verify_jwt)):
    return update_or_create_opa_data(opa_config.data, opa_config.name)


@opaConfigRouter.delete("/policies/{policy_name}", response_model=bool)
def delete_policy(policy_name: str, db_user=Depends(verify_jwt)):
    if policy_name not in get_policies():
        raise HTTPException(status_code=404, detail="Policy not found")
    return delete_opa_policy(policy_name)


@opaConfigRouter.post("/policies/check")
def check_policies(opa_policy_check: OPAPolicyCheck, db_user=Depends(verify_jwt)):
    if opa_policy_check.policy_name not in get_policies():
        raise HTTPException(status_code=404, detail="Policy not found")
    return check_policy(opa_policy_check.policy_name, opa_policy_check.rule_name, opa_policy_check.input_data)
