from typing import Any, Dict
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.schemas.app import App
import api.services.monitoring_service as MonitoringService
from api.db.database import get_db
from api.routes.auth_routes import verify_jwt
from api.services.alert_service import processAlert
monitoringRouter = APIRouter()


@monitoringRouter.post("/", tags=["app"], description="Start Monitoring", response_model_exclude_none=True)
async def start(db_user=Depends(verify_jwt)):
    apps = await MonitoringService.start_monitoring()
    return apps


@monitoringRouter.post("/stop", tags=["app"], description="Stop Monitoring", response_model_exclude_none=True)
async def stop(db_user=Depends(verify_jwt)):
    apps = await MonitoringService.stop_monitoring()
    return apps


@monitoringRouter.post("/restart", tags=["app"], description="Restart Monitoring", response_model_exclude_none=True)
async def restart(db_user=Depends(verify_jwt)):
    apps = await MonitoringService.restart_monitoring()
    return apps


@monitoringRouter.post("/alert", tags=["app"], description="Alert an app")
async def alert(data: Dict[Any, Any]):
    return await processAlert(data)
