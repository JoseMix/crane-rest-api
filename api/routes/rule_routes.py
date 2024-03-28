from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.schemas.app import App
import api.services.rule_service as RuleService
from api.db.database import get_db
from api.routes.auth_routes import verify_jwt

ruleRouter = APIRouter()


@ruleRouter.post("/", tags=["app"], description="Start Rule", response_model_exclude_none=True)
async def start(db_user=Depends(verify_jwt)):
    apps = await RuleService.start_rules()
    return apps


@ruleRouter.post("/stop", tags=["app"], description="Stop Rule", response_model_exclude_none=True)
async def stop(db_user=Depends(verify_jwt)):
    apps = await RuleService.stop_rules()
    return apps


@ruleRouter.post("/restart", tags=["app"], description="Restart Rule", response_model_exclude_none=True)
async def restart(db_user=Depends(verify_jwt)):
    apps = await RuleService.restart_rules()
    return apps
