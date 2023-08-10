from typing import Any, Dict
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.schemas.app import App
import api.services.crane_service as CraneService
from api.clients.OPAClient import check_policy, create_policy
from api.db.database import get_db
from api.routes.auth_routes import verify_jwt
appRouter = APIRouter()


@appRouter.get("/", tags=["app"], description="Get all apps", response_model_exclude_none=True)
async def get(db_user=Depends(verify_jwt), db: Session = Depends(get_db)):
    apps = await CraneService.get_apps(db, db_user)
    return apps


@appRouter.post("/", tags=["app"], description="Create a new app")
async def create(app: App, db_user=Depends(verify_jwt), db: Session = Depends(get_db)):
    app = await CraneService.create(db, app, db_user)
    return app


@appRouter.patch("/", tags=["app"], description="Update an app")
async def update(app: App, db_user=Depends(verify_jwt), db: Session = Depends(get_db)):
    app = await CraneService.update(db, app, db_user)
    return app


@appRouter.delete("/", tags=["app"], description="Delete an app")
async def delete(app: App, db_user=Depends(verify_jwt), db: Session = Depends(get_db)):
    app = await CraneService.delete(db, app, db_user)
    return app


@appRouter.post("/start", tags=["app"], description="Get all apps", response_model_exclude_none=True)
async def start(db_user=Depends(verify_jwt)):
    apps = await CraneService.start_monitoring()
    return apps


@appRouter.post("/scale", tags=["app"], description="Scale an app")
async def scale(app: App, db_user=Depends(verify_jwt)):
    current_app = await CraneService.scale(app, db_user)
    return current_app


@appRouter.post("/alert", tags=["app"], description="Alert an app")
async def alert(data: Dict[Any, Any]):
    print(data)
    return " ***************-----------  alert ----------------****************"


@appRouter.post("/stop", tags=["app"], description="Stop an app")
async def stop(app: App, db_user=Depends(verify_jwt)):
    current_app = await CraneService.stop(app, db_user)
    return current_app


@appRouter.post("/restart", tags=["app"], description="Restart an app")
async def restart(app: App, db_user=Depends(verify_jwt)):
    current_app = await CraneService.restart(app, db_user)
    return current_app


@appRouter.post("/logs", tags=["app"], description="Get logs for an app")
async def logs(app: App, db_user=Depends(verify_jwt)):
    logs = await CraneService.logs(app, db_user)
    return logs


@appRouter.post("/opa", tags=["app"], description="Create OPA policy for an app")
async def opa(app: App, db_user=Depends(verify_jwt)):
    # Usar el método check_policy
    input_data = {"user": "Alice", "action": "read", "object": "document1"}
    check_policy(input_data)

    # Usar el método create_policy
    policy_data = {
        "policy": {
            "default": {
                "allow": {
                    "rule": {"user": "Alice", "action": "read", "object": "document1"}
                }
            }
        }
    }
    create_policy(policy_data)
