from fastapi import APIRouter
from schemas.app import App
from services.manage import get_apps, create_app, scale_app

manage = APIRouter()


@manage.get("/apps", tags=["app"], description="Get all apps")
async def getApps():
    apps = await get_apps()
    return apps


@manage.post("/apps", tags=["app"], description="Create a new app")
async def createApp(app: App):
    new_app = await create_app(app)
    return new_app


@manage.post("/apps/scale", tags=["app"], description="Scale an app")
async def scaleApp(app: App):
    current_app = await scale_app(app)
    return current_app
