from re import search
from schemas.app import App
from clients import DockerClient
from services.pycompose import docker_compose_generator, prometheus_yaml_generator, prometheus_scrape_generator


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
        apps.append(App(
            name=container.name,
            id=container.id,
        ))

    return apps


async def get_apps():
    docker = await DockerClient.get_client("all")
    containers = docker.ps()
    apps = []
    for container in containers:
        apps.append(App(
            name=container.name,
            id=container.id,
        ))
    return apps


async def create_app(app: App):
    await docker_compose_generator(app)
    docker = await DockerClient.get_client(app.name)
    docker.compose.build()
    docker.compose.up(detach=True)
    containers = docker.ps()
   
    search = [container for container in containers if container.name.startswith(
        app.name + "-traefik")]

    app.ip = search[0].network_settings.networks['prometheus-net'].ip_address
    
    await prometheus_scrape_generator(app)
    docker = await DockerClient.get_client("monitoring")
    docker.compose.stop()
    docker.compose.up(detach=True)

    return app


async def scale_app(app: App):
    docker = await DockerClient.get_client(app.name)
    scales = {service['name']: service['count'] for service in app.services}
    docker.compose.up(detach=True, scales=scales)
    return app
