from typing import Any, Dict
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.schemas.app import App
from api.services.crane_service import get_apps, create_app, scale_app, start_crane
from api.db.database import get_db
from api.routes.auth_routes import verify_jwt
appRouter = APIRouter()


@appRouter.get("/", tags=["app"], description="Get all apps", response_model_exclude_none=True)
async def get(db_user=Depends(verify_jwt), db: Session = Depends(get_db)):
    apps = await get_apps(db, db_user)
    return apps


@appRouter.post("/", tags=["app"], description="Create a new app")
async def create(app: App, db_user=Depends(verify_jwt), db: Session = Depends(get_db)):
    app = await create_app(db, app, db_user)
    return app


@appRouter.post("/start", tags=["app"], description="Get all apps", response_model_exclude_none=True)
async def start(db_user=Depends(verify_jwt)):
    apps = await start_crane()
    return apps


@appRouter.post("/scale", tags=["app"], description="Scale an app")
async def scale(app: App, db_user=Depends(verify_jwt)):
    current_app = await scale_app(app, db_user)
    return current_app


@appRouter.post("/alert", tags=["app"], description="Alert an app")
async def alert(data: Dict[Any, Any]):
    print(data)
    return " ***************-----------  alert ----------------****************"
