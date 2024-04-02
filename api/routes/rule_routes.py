''' This module contains the routes for the rule service '''
from fastapi import APIRouter, Depends
import api.services.rule_service as RuleService
from api.routes.auth_routes import verify_jwt

ruleRouter = APIRouter()


@ruleRouter.post("/", tags=["app"], description="Start Rule", response_model_exclude_none=True, dependencies=[Depends(verify_jwt)])
async def start():
    ''' Start Open Policy Agent service '''
    apps = await RuleService.start_rules()
    return apps


@ruleRouter.post("/stop", tags=["app"], description="Stop Rule", response_model_exclude_none=True, dependencies=[Depends(verify_jwt)])
async def stop():
    ''' Stop Open Policy Agent service '''
    apps = await RuleService.stop_rules()
    return apps


@ruleRouter.post("/restart", tags=["app"], description="Restart Rule", response_model_exclude_none=True, dependencies=[Depends(verify_jwt)])
async def restart():
    ''' Restart Open Policy Agent service '''
    apps = await RuleService.restart_rules()
    return apps
