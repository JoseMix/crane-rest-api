from glob import glob
from python_on_whales import DockerClient, docker
from pathlib import Path
import subprocess
import platform
from api.config.constants import TEMP_FILES_PATH, MONITORING_FILES_PATH



def is_docker_daemon_running():
    try:
        subprocess.check_output("docker ps".split())
        return True
    except subprocess.CalledProcessError:
        return False


def start_docker_daemon():
    print("Starting Docker daemon...")
    print(platform.system())
    if platform.system() == "Linux":
        command = "service docker start"
    elif platform.system() == "Windows":
        return "Error: Docker daemon cannot be started automatically on Windows. Please start it manually."
    else:
        return "Error: Unsupported platform. Please start Docker daemon manually."

    try:
        subprocess.check_output(command.split())
        return True
    except subprocess.CalledProcessError:
        return False


async def get_client(project_name):
    if not is_docker_daemon_running():
        result = start_docker_daemon()
        if result != True:
            raise Exception(result)

    if (project_name == 'all'):
        return docker
    elif (project_name == 'monitoring'):
        client = DockerClient(compose_files=glob(
            f'{Path.cwd()}/{MONITORING_FILES_PATH}/*.yml')
        )
    else:
        client = DockerClient(compose_files=glob(
            f'{Path.cwd()}/{TEMP_FILES_PATH}/{project_name}/*.yml')
        )
    return client
