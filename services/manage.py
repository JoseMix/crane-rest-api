from schemas.app import App
from clients import DockerClient
from services.pycompose import docker_compose_generator


async def get_apps():
    docker = await DockerClient.get_client("all")
    containers = docker.ps()
    apps = []
    for container in containers:
        apps.append(App(
            name=container.name,
            id=container.id
        ))
    return apps


async def create_app(app: App):
    await docker_compose_generator(app)
    docker = await DockerClient.get_client(app.name)
    docker.compose.build()
    docker.compose.up(detach=True)
    return app


async def scale_app(app: App):
    docker = await DockerClient.get_client(app.name)
    scales = {service['name']: service['count'] for service in app.services}
    docker.compose.up(detach=True, scales=scales)
    return app
