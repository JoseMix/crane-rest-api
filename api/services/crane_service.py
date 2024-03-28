from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import List
import uuid
import json
import api.db.crud.app_crud as AppCrud
from api.schemas.app import App, AppDocker
from api.clients import DockerClient
from api.config.constants import *
from api.services.generator_service import docker_compose_generator, docker_compose_remove, prometheus_scrape_generator, prometheus_scrape_remove
from api.services.monitoring_service import restart_monitoring


async def get_app_by_id(db, db_user, app_id: int):
    app = AppCrud.get_by_id(db, db_user, app_id)
    if not app:
        raise HTTPException(status_code=404, detail="App not found")
    app.services = json.loads(app.services)
    app = {k: v for k, v in app.__dict__.items() if v is not None}
    return app


async def get_app_with_docker(db, db_user, app_id: int):
    app = await get_app_by_id(db, db_user, app_id)
    app = AppDocker(**app)
    docker_compose_generator(app)
    app.docker = await DockerClient.get_client(app.name)
    return app


async def get_all(db, db_user, skip: int = 0, limit: int = 100):
    apps = AppCrud.get_all(db, db_user, skip, limit)
    for app in apps:
        app.services = json.loads(app.services)
        app.hosts = json.loads(app.hosts)
        app.ports = json.loads(app.ports)
    return apps


async def create(db: Session, app: App, db_user):
    app.name = f"{app.name}-{uuid.uuid4().hex[:8]}"
    db_app = AppCrud.get_by_name(db, db_user,  app.name)
    if db_app:
        raise HTTPException(
            status_code=400, detail="App with this name already exists")

    app.user_id = db_user.id

    # create app in db
    db_app = AppCrud.create(db, app)

    # create docker compose file and start app
    compose = docker_compose_generator(app)
    docker = await DockerClient.get_client(app.name)
    docker.compose.build()
    docker.compose.up(detach=True)
    containers = docker.ps(filters={"name": app.name})

    # get traefik container
    search = [container for container in containers if container.name.startswith(
        app.name + "-traefik")]

    # get traefik ip
    app.ip = search[0].network_settings.networks[PROMETHEUS_NETWORK_NAME].ip_address
    app.port = search[0].network_settings.ports['80/tcp'][0]['HostPort']
    app.ports = search[0].network_settings.ports
    app.hosts = compose['hosts']
    AppCrud.update(db, db_user, db_app.id, app)

    # create prometheus yaml file
    prometheus_scrape_generator(app)

    # restart monitoring docker compose
    await restart_monitoring()

    # por ultimo eliminar el docker compose temporal generado para la app
    docker_compose_remove(app.name)

    # finally return app
    return db_app


async def start(db: Session, app_id: str, db_user):
    app = await get_app_with_docker(db, db_user, app_id)
    app.docker.compose.build()
    app.docker.compose.up(detach=True)
    docker_compose_remove(app.name)
    return {"message": f"App {app.name} started"}


async def scale(db: Session, app_id: str, db_user):
    app = await get_app_with_docker(db, db_user, app_id)
    scales = {service['name']: service['count']
              for service in app.services}
    app.docker.compose.up(detach=True, scales=scales)
    return {"message": f"App {app.name} scaled"}


async def update(db: Session, app_id: str, app: App, db_user):
    AppCrud.update(db, db_user, app_id, app)
    return {"message": f"App {app.name} updated"}


async def restart(db: Session, app_id: str, db_user):
    app = await get_app_with_docker(db, db_user, app_id)
    app.docker.compose.restart()
    return {"message": f"App {app.name} restarted"}


async def stop(db: Session, app_id: str, db_user):
    app = await get_app_with_docker(db, db_user, app_id)
    app.docker.compose.stop()
    docker_compose_remove(app.name)
    return {"message": f"App {app.name} stopped"}


async def delete(db: Session, app_id: str, db_user):
    app = await get_app_with_docker(db, db_user, app_id)
    app.docker.compose.down()
    docker_compose_remove(app.name)
    prometheus_scrape_remove(app.name)
    await restart_monitoring()
    AppCrud.delete_physical(db, db_user, app.name)
    return {"message": f"App {app.name} deleted"}


async def logs(db: Session, app_id: str, db_user):
    app = await get_app_with_docker(db, db_user, app_id)
    return app.docker.compose.logs()


async def stats(db: Session, app_id: str, db_user):
    app = await get_app_with_docker(db, db_user, app_id)
    app_stats = app.docker.stats()
    app_stats = [
        service for service in app_stats if service.container_name.startswith(app.name)
    ]
    return app_stats
