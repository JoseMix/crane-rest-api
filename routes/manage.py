from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter
from clients import DockerClient
from schemas.base_app import BaseApp
from schemas.scale import Scale

from schemas.container import Container

manage = APIRouter()


@manage.post("/app", tags=["app"], response_model=BaseApp, description="Create a new app")
def create_app(app: BaseApp):
    container = DockerClient.create_app(app.image, app.name)
    return JSONResponse(content=jsonable_encoder(container.attrs))


@manage.get("/containers",  tags=["containers"], description="Get all containers")
async def get_container_list():
    list = await DockerClient.get_container_list()
    # iterate over list and return attrs of each container
    return [container.attrs for container in list]


@manage.get("/networks",  tags=["containers"], description="Get all containers")
async def get_network_list():
    list = await DockerClient.get_network_list()
    return [network.attrs for network in list]


@manage.post("/containers", tags=["app"], response_model=BaseApp, description="Create a new app")
def create_app(app: BaseApp):
    container = DockerClient.create_container(app.image, app.name)
    return JSONResponse(content=jsonable_encoder(container.attrs))