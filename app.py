from fastapi import FastAPI, APIRouter
from dotenv import load_dotenv
from api.routes.apps_routes import appRouter
from api.routes.users_routes import userRouter
from api.routes.auth_routes import authRouter

load_dotenv()

app = FastAPI()

v1_router = APIRouter()
v1_router.include_router(authRouter, prefix="/auth")
v1_router.include_router(userRouter, prefix="/users")
v1_router.include_router(appRouter, prefix="/apps")

app.include_router(v1_router, prefix="/api/v1")
