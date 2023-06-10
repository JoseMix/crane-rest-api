from fastapi import HTTPException
from api.schemas.app import App
from api.clients import DockerClient
from sqlalchemy.orm import Session
from api.services.generator_service import docker_compose_generator, prometheus_yaml_generator, prometheus_scrape_generator
from api.db.crud import create_user_app, get_services, get_service_by_name_and_user


async def start_crane():
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


async def get_apps(db, db_user):
    user_apps = get_services(db, db_user)
    return user_apps
    docker = await DockerClient.get_client("all")
    containers = docker.ps()
    apps = []
    for container in containers:
        apps.append(App(
            name=container.name,
            id=container.id,
        ))
    return apps


async def create_app(db: Session, app: App, db_user):
    # first validate if the user app exists with the same name
    db_app = get_service_by_name_and_user(db, app.name, db_user)
    if db_app:
        raise HTTPException(
            status_code=400, detail="App with this name already exists")
    await docker_compose_generator(app)
    docker = await DockerClient.get_client(app.name)
    docker.compose.build()
    docker.compose.up(detach=True)
    containers = docker.ps()

    search = [container for container in containers if container.name.startswith(
        app.name + "-traefik")]

    app.ip = search[0].network_settings.networks['prometheus-net'].ip_address
    app.user_id = db_user.id
    db_app = create_user_app(db, app, db_user)

    await prometheus_scrape_generator(app)
    docker = await DockerClient.get_client("monitoring")
    docker.compose.stop()
    docker.compose.up(detach=True)
    return db_app


async def scale_app(app: App):
    docker = await DockerClient.get_client(app.name)
    scales = {service['name']: service['count'] for service in app.services}
    docker.compose.up(detach=True, scales=scales)
    return app
