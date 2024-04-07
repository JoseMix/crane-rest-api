from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.schemas.app import App
import api.services.crane_service as CraneService
from api.db.database import get_db
from api.routes.auth_routes import verify_jwt

appRouter = APIRouter()


@appRouter.get("/", tags=["app"], description="Get all apps", response_model_exclude_none=True)
async def get(db_user=Depends(verify_jwt), db: Session = Depends(get_db)):
    ''' Get all user apps '''
    apps = await CraneService.get_apps_with_docker(db, db_user.id)
    return apps


@appRouter.post("/", tags=["app"], description="Create a new app")
async def create(app: App, db_user=Depends(verify_jwt), db: Session = Depends(get_db)):
    ''' Create a new app '''
    app = await CraneService.create(db, app, db_user.id)
    return app


@appRouter.patch("/{app_id}", tags=["app"], description="Update an app")
async def update(app_id: str, app: App, db_user=Depends(verify_jwt), db: Session = Depends(get_db)):
    ''' Update an app '''
    app = await CraneService.update(db, app_id, app, db_user.id)
    return app


@appRouter.get("/{app_id}", tags=["app"], description="Get an app", response_model_exclude_none=True)
async def get_app(app_id: str, db_user=Depends(verify_jwt), db: Session = Depends(get_db)):
    ''' Get an app '''
    app = await CraneService.get_app_by_id(db, app_id, db_user.id)
    return app


@appRouter.delete("/{app_id}", tags=["app"], description="Delete an app")
async def delete(app_id: str, db_user=Depends(verify_jwt), db: Session = Depends(get_db)):
    ''' Delete an app '''
    app = await CraneService.delete(db, app_id, db_user.id)
    return app


@appRouter.post("/{app_id}/start", tags=["app"], description="Start app")
async def start(app_id: str, db_user=Depends(verify_jwt), db: Session = Depends(get_db)):
    ''' Start services of the app '''
    app = await CraneService.start(db, app_id, db_user.id)
    return app


@appRouter.post("/{app_id}/stop", tags=["app"], description="Stop app")
async def stop(app_id: int, db_user=Depends(verify_jwt), db: Session = Depends(get_db)):
    ''' Stop services of the app '''
    app = await CraneService.stop(db, app_id, db_user.id)
    return app


@appRouter.post("/{app_id}/scale", tags=["app"], description="Scale app")
async def scale(app_id: str, db_user=Depends(verify_jwt), db: Session = Depends(get_db)):
    ''' Generate a new instance of the app services '''
    app = await CraneService.scale(db, app_id, db_user.id)
    return app


@appRouter.post("/{app_id}/restart", tags=["app"], description="Restart app")
async def restart(app_id: str, db_user=Depends(verify_jwt), db: Session = Depends(get_db)):
    ''' Restart services of the app '''
    app = await CraneService.restart(db, app_id, db_user.id)
    return app


@appRouter.post("/{app_id}/logs", tags=["app"], description="Get logs for app")
async def logs(app_id: str, db_user=Depends(verify_jwt), db: Session = Depends(get_db)):
    ''' Get logs for the app '''
    app_logs = await CraneService.logs(db, app_id, db_user.id)
    return app_logs


@appRouter.post("/{app_id}/stats", tags=["app"], description="Get stats for app")
async def stats(app_id: str, db_user=Depends(verify_jwt), db: Session = Depends(get_db)):
    ''' Get stats for the app '''
    app_stats = await CraneService.stats(db, app_id, db_user.id)
    return app_stats


@appRouter.post("/refresh", tags=["app"], description="Refresh apps", dependencies=[Depends(verify_jwt)])
async def refresh(db: Session = Depends(get_db)):
    ''' Refresh apps scrapes on prometheus yaml and database '''
    apps = await CraneService.refresh_apps_scrapes(db)
    return apps
