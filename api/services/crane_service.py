''' This module contains the services for the crane app. '''
import uuid
import json
from fastapi import HTTPException
from sqlalchemy.orm import Session
import api.db.crud.app_crud as AppCrud
from api.schemas.app import App, AppDocker
from api.clients import DockerClient
from api.config.constants import PROMETHEUS_NETWORK_NAME
from api.services.generator_service import docker_compose_generator, docker_compose_remove, prometheus_scrape_generator, prometheus_scrape_remove
from api.services.monitoring_service import restart_monitoring


async def create(db: Session, app: App, user_id: int):
    ''' Create a new app '''
    app.name = f"{app.name}-{uuid.uuid4().hex[:8]}"
    db_app = AppCrud.get_by_name(db, app.name, user_id)
    if db_app:
        raise HTTPException(
            status_code=400, detail="App with this name already exists")

    app.user_id = user_id

    # create app in db
    db_app = AppCrud.create(db, app)

    # create docker compose file and start app
    compose = docker_compose_generator(app)
    docker = await DockerClient.get_client(app.name)
    docker.compose.build()
    docker.compose.up(detach=True)

    # get traefik container ip and ports
    traefik_ip, traefik_ports = await get_router_dir(app, docker)
    app.ip = traefik_ip
    app.port = traefik_ports['80/tcp'][0]['HostPort']
    app.ports = traefik_ports
    app.hosts = compose['hosts']

    # update app in db
    AppCrud.update(db, db_app.id, app, user_id)

    # create prometheus yaml file
    prometheus_scrape_generator(app)

    # restart monitoring docker compose
    await restart_monitoring()

    # por ultimo eliminar el docker compose temporal generado para la app
    docker_compose_remove(app.name)

    # finally return app
    return db_app


async def start(db: Session, app_id: str, user_id: int = None):
    ''' Start docker compose for app '''
    app = await get_app_with_docker(db, app_id, user_id)
    app.docker.compose.build()
    app.docker.compose.up(detach=True)
    docker_compose_remove(app.name)
    return {"message": f"App {app.name} started"}


async def scale(db: Session, app_id: str, count: int, user_id: int = None):
    ''' Scale app services '''
    app = await get_app_with_docker(db, app_id, user_id)
    scales = {service['name']: count for service in app.services}
    app.docker.compose.up(detach=True, scales=scales)
    return {"message": f"App {app.name} scaled"}


async def update(db: Session, app_id: str, app: App, user_id: int):
    ''' Update app on db and docker compose '''
    AppCrud.update(db, app_id, app, user_id)
    return {"message": f"App {app.name} updated"}


async def restart(db: Session, app_id: str, user_id: int):
    ''' Restart app services '''
    app = await get_app_with_docker(db, app_id, user_id)
    app.docker.compose.restart()
    return {"message": f"App {app.name} restarted"}


async def stop(db: Session, app_id: str, user_id: int):
    ''' Stop app services '''
    app = await get_app_with_docker(db, app_id, user_id)
    app.docker.compose.stop()
    docker_compose_remove(app.name)
    return {"message": f"App {app.name} stopped"}


async def delete(db: Session, app_id: str, user_id: int):
    ''' Delete app on db and docker compose '''
    app = await get_app_with_docker(db, app_id, user_id)
    app.docker.compose.down()
    docker_compose_remove(app.name)
    prometheus_scrape_remove(app.name)
    await restart_monitoring()
    AppCrud.delete_physical(db, app.name, user_id)
    return {"message": f"App {app.name} deleted"}


async def logs(db: Session, app_id: str, user_id: int):
    ''' Get logs for app services containers '''
    app = await get_app_with_docker(db, app_id, user_id)
    return app.docker.compose.logs()


async def stats(db: Session, app_id: str, user_id: int):
    ''' Get stats for app services containers '''
    app = await get_app_with_docker(db, app_id, user_id)
    app_stats = app.docker.stats()
    app_stats = [
        service for service in app_stats if service.container_name.startswith(app.name)
    ]
    return app_stats


async def get_app_by_id(db, app_id: int, user_id: int = None):
    ''' Get app by id '''
    app = AppCrud.get_by_id(db, app_id, user_id)
    if not app:
        raise HTTPException(status_code=404, detail="App not found")
    app.services = json.loads(app.services)
    app = {k: v for k, v in app.__dict__.items() if v is not None}
    return app


async def get_app_with_docker(db, app_id: int, user_id: int = None):
    ''' Get app by id with docker client '''
    app = await get_app_by_id(db, app_id, user_id)
    app = AppDocker(**app)
    docker_compose_generator(app)
    app.docker = await DockerClient.get_client(app.name)
    return app


async def get_app_by_name(db, app_name: str, user_id: int):
    ''' Get app by name '''
    app = AppCrud.get_by_name(db, app_name, user_id)
    if not app:
        raise HTTPException(status_code=404, detail="App not found")
    app.services = json.loads(app.services)
    app = {k: v for k, v in app.__dict__.items() if v is not None}
    return app


async def get_all(db, user_id: int, skip: int = 0, limit: int = 100):
    ''' Get all apps '''
    apps = AppCrud.get_all(db, user_id, skip, limit)
    for app in apps:
        app.services = json.loads(app.services)
        app.hosts = json.loads(app.hosts)
        app.ports = json.loads(app.ports)
    return apps


async def get_router_dir(app, docker):
    ''' Get traefik container ip and ports '''
    containers = docker.ps(filters={"name": app.name})
    if not containers:
        return None, None
    traefik_container = [container for container in containers if container.name.startswith(
        app.name + "-traefik")][0]
    traefik_ip = traefik_container.network_settings.networks[PROMETHEUS_NETWORK_NAME].ip_address
    traefik_ports = traefik_container.network_settings.ports
    return traefik_ip, traefik_ports


async def refresh_apps_scrapes(db: Session):
    ''' Refresh apps prometheus scrapes '''
    apps = AppCrud.get_all(db, None)
    for app in apps:
        app.services = json.loads(app.services)
        app = {k: v for k, v in app.__dict__.items() if v is not None}
        app = AppDocker(**app)
        compose = docker_compose_generator(app)
        docker = await DockerClient.get_client(app.name)

        traefik_ip, traefik_ports = await get_router_dir(app, docker)
        app.ip = traefik_ip
        app.port = traefik_ports['80/tcp'][0]['HostPort']
        app.ports = traefik_ports
        app.hosts = compose['hosts']
        AppCrud.update(db, app.id, app)
        prometheus_scrape_generator(app)

    await restart_monitoring()
    return {"message": "Apps refreshed"}
