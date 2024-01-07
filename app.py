from api.utils.docker import verify_docker_daemon
from api.routes.opa_routes import opaConfigRouter
from api.routes.auth_routes import authRouter
from api.routes.apps_routes import appRouter
from api.routes.monitoring_routes import monitoringRouter
from dotenv import load_dotenv
from fastapi import FastAPI, APIRouter
from logging.config import dictConfig
from api.config.logger import LogConfig
dictConfig(LogConfig().dict())


verify_docker_daemon()
load_dotenv()
app = FastAPI()

v1_router = APIRouter()
v1_router.include_router(authRouter, prefix="/auth")
v1_router.include_router(monitoringRouter, prefix="/monitoring")
v1_router.include_router(appRouter, prefix="/apps")
v1_router.include_router(opaConfigRouter, prefix="/opa")

app.include_router(v1_router, prefix="/api/v1")
