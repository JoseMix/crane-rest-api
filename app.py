from api.utils.docker import verify_docker_daemon
from api.routes.opa_routes import opaConfigRouter
from api.routes.auth_routes import authRouter
from api.routes.apps_routes import appRouter
from api.routes.role_routes import roleRouter
from api.routes.monitoring_routes import monitoringRouter
from dotenv import load_dotenv
from fastapi import FastAPI, APIRouter
from logging.config import dictConfig
from api.config.logger import LogConfig
from api.config.constants import API_PREFIX

dictConfig(LogConfig().dict())


verify_docker_daemon()
load_dotenv()
app = FastAPI()

router = APIRouter()
router.include_router(authRouter, prefix="/v1/auth")
router.include_router(monitoringRouter, prefix="/v1/monitoring")
router.include_router(appRouter, prefix="/v1/apps")
router.include_router(opaConfigRouter, prefix="/v1/opa")
router.include_router(roleRouter, prefix="/v1/roles")


app.include_router(router, prefix=API_PREFIX)
