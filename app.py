import asyncio
from dotenv import load_dotenv
from fastapi import FastAPI, APIRouter
from logging.config import dictConfig
from api.config.logger import LogConfig
from api.utils.docker import docker_running
from api.routes.opa_routes import opaConfigRouter
from api.routes.auth_routes import authRouter
from api.routes.apps_routes import appRouter
from api.routes.role_routes import roleRouter
from api.routes.monitoring_routes import monitoringRouter
from api.routes.rule_routes import ruleRouter
from api.config.constants import API_PREFIX, OPA_RBAC_CONFIG_NAME, OPA_RBAC_CONFIG_FILE
from api.clients.OPAClient import update_policies_file
from api.services.rule_service import start_rules
from api.services.monitoring_service import start_monitoring

dictConfig(LogConfig().dict())
load_dotenv()
app = FastAPI()


# Verify Docker daemon is running
if not docker_running():
    exit(0)


@app.on_event("startup")
async def startup_event():
    await start_rules()
    await start_monitoring()
    update_policies_file(OPA_RBAC_CONFIG_NAME, OPA_RBAC_CONFIG_FILE, True)


router = APIRouter()
router.include_router(authRouter, prefix="/v1/auth")
router.include_router(ruleRouter, prefix="/v1/rules")
router.include_router(monitoringRouter, prefix="/v1/monitoring")
router.include_router(appRouter, prefix="/v1/apps")
router.include_router(opaConfigRouter, prefix="/v1/opa")
router.include_router(roleRouter, prefix="/v1/roles")

app.include_router(router, prefix=API_PREFIX)
