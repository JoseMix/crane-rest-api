from typing import Any, Dict
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.schemas.app import App
import api.services.crane_service as CraneService
from api.db.database import get_db
from api.routes.auth_routes import verify_jwt

appRouter = APIRouter()


@appRouter.get("/", tags=["app"], description="Get all apps", response_model_exclude_none=True)
async def get(db_user=Depends(verify_jwt), db: Session = Depends(get_db)):
    apps = await CraneService.get_all(db, db_user)
    return apps


@appRouter.post("/", tags=["app"], description="Create a new app")
async def create(app: App, db_user=Depends(verify_jwt), db: Session = Depends(get_db)):
    app = await CraneService.create(db, app, db_user)
    return app


@appRouter.patch("/{app_id}", tags=["app"], description="Update an app")
async def update(app_id: str, app: App, db_user=Depends(verify_jwt), db: Session = Depends(get_db)):
    app = await CraneService.update(db, app_id, app, db_user)
    return app


@appRouter.get("/{app_id}", tags=["app"], description="Get an app", response_model_exclude_none=True)
async def get_app(app_id: str, db_user=Depends(verify_jwt), db: Session = Depends(get_db)):
    app = await CraneService.get_app_by_id(db, db_user, app_id)
    return app


@appRouter.delete("/{app_id}", tags=["app"], description="Delete an app")
async def delete(app_id: str, db_user=Depends(verify_jwt), db: Session = Depends(get_db)):
    app = await CraneService.delete(db, app_id, db_user)
    return app


@appRouter.post("/{app_id}/start", tags=["app"], description="Start app")
async def start(app_id: str, db_user=Depends(verify_jwt), db: Session = Depends(get_db)):
    app = await CraneService.start(db, app_id, db_user)
    return app


@appRouter.post("/{app_id}/stop", tags=["app"], description="Stop app")
async def stop(app_id: int, db_user=Depends(verify_jwt), db: Session = Depends(get_db)):
    app = await CraneService.stop(db, app_id, db_user)
    return app


@appRouter.post("/{app_id}/scale", tags=["app"], description="Scale app")
async def scale(app_id: str, db_user=Depends(verify_jwt), db: Session = Depends(get_db)):
    app = await CraneService.scale(db, app_id, db_user)
    return app


@appRouter.post("/{app_id}/restart", tags=["app"], description="Restart app")
async def restart(app_id: str, db_user=Depends(verify_jwt), db: Session = Depends(get_db)):
    app = await CraneService.restart(db, app_id, db_user)
    return app


@appRouter.post("/{app_id}/logs", tags=["app"], description="Get logs for app")
async def logs(app_id: str, db_user=Depends(verify_jwt), db: Session = Depends(get_db)):
    logs = await CraneService.logs(db, app_id, db_user)
    return logs

@appRouter.post("/{app_id}/stats", tags=["app"], description="Get stats for app")
async def stats(app_id: str, db_user=Depends(verify_jwt), db: Session = Depends(get_db)):
    stats = await CraneService.stats(db, app_id, db_user)
    return stats