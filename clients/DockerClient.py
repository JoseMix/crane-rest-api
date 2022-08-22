from glob import glob
from python_on_whales import DockerClient, docker
from pathlib import Path


async def get_client(project_name):
    if(project_name == 'all'):
        print("Getting all clients")
        return docker
    else:
        print("Getting client for {}".format(project_name))
        client = DockerClient(compose_files=glob(
            f'{Path.cwd()}/composes/{project_name}/*.yml')
        )
        return client
