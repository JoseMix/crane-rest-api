from fastapi import HTTPException
from api.schemas.app import App
from api.clients import DockerClient
from sqlalchemy.orm import Session
from api.services.generator_service import docker_compose_generator, prometheus_yaml_generator, prometheus_scrape_generator
import api.db.crud.app_crud as AppCrud


async def start_monitoring():
    # create network
    docker = await DockerClient.get_client("all")
    networks = docker.network.list()
    search = [network for network in networks if network.name == "prometheus-net"]

    if not search:
        docker.network.create('prometheus-net', driver="bridge")

    # start del docker compose de prometheus y alertmanager
    docker = await DockerClient.get_client("monitoring")
    docker.compose.up(detach=True)

    containers = docker.ps()
    apps = []
    await prometheus_yaml_generator()

    for container in containers:
        apps.append(
            App(
                name=container.name,
                id=container.id,
                services=[],
            ))

    return apps


async def get_apps(db, db_user, skip: int = 0, limit: int = 100):
    user_apps = AppCrud.get_all(db, db_user, skip, limit)
    apps = []

    # Reuse Docker client
    docker = await DockerClient.get_client('all')

    for user_app in user_apps:
        # Filter containers in Docker query
        containers = docker.ps(filters={"name": user_app.name})

        app = App(
            name=user_app.name,
            id=user_app.id,
            services=[container.name for container in containers],
        )
        apps.append(app)
    return apps


async def create(db: Session, app: App, db_user):
    # create app name with user_id and app_name
    app.name = f"{db_user.id}-{app.name}"
    db_app = AppCrud.get_by_name(db, app.name, db_user)
    if db_app:
        raise HTTPException(
            status_code=400, detail="App with this name already exists")

    # create docker compose file and start app
    await docker_compose_generator(app)
    docker = await DockerClient.get_client(app.name)
    docker.compose.build()
    docker.compose.up(detach=True)
    containers = docker.ps(filters={"name": app.name})

    # get traefik container
    search = [container for container in containers if container.name.startswith(
        app.name + "-traefik")]

    # get traefik ip
    app.ip = search[0].network_settings.networks['prometheus-net'].ip_address

    app.user_id = db_user.id

    # create app in db
    db_app = AppCrud.create(db, app)

    # create prometheus yaml file
    await prometheus_scrape_generator(app)

    # restart monitoring docker compose
    docker = await DockerClient.get_client("monitoring")
    docker.compose.stop()
    docker.compose.up(detach=True)

    # finally return app
    return db_app


async def scale(app: App):
    docker = await DockerClient.get_client(app.name)
    scales = {service['name']: service['count'] for service in app.services}
    docker.compose.up(detach=True, scales=scales)
    return app


async def start(app: App):
    # find app in db
    db_app = AppCrud.get_by_name(app.name, app.user_id)
    if not db_app:
        raise HTTPException(status_code=404, detail="App not found")
    docker = await DockerClient.get_client(app.name)
    docker.compose.up(detach=True)
    return app


async def update(app: App):
    updated = AppCrud.update(app)
    return updated


async def restart(app: App):
    docker = await DockerClient.get_client(app.name)
    docker.compose.restart()
    return app


async def stop(app: App):
    docker = await DockerClient.get_client(app.name)
    docker.compose.stop()
    return app


async def delete(app: App):
    docker = await DockerClient.get_client(app.name)
    docker.compose.down()
    # delete_at from db
    AppCrud.delete_logical(app)


async def logs(app: App):
    docker = await DockerClient.get_client(app.name)
    return docker.compose.logs()
