from concurrent.futures import process
import docker
from dotenv import dotenv_values
import subprocess
config = dotenv_values(".env")
client = docker.from_env()

# *********************** containers ***********************


def create_app(image, name):

    # create network
    # start proxy container using traefik
    # start image selected for user
    # return host and port of proxy container

    client.containers.run('traefik:v2.7',
                          name='traefik',
                          detach=True,
                          command='--api.insecure=true --providers.docker',
                          ports={'8080/tcp': 8080, '80/tcp': 80},
                          volumes={'/var/run/docker.sock': {'bind': '/var/run/docker.sock', 'mode': 'rw'}
                                   }
                          )
    return client.containers.run(image, name=name, detach=True, labels={
        "traefik.http.routers.whoami.rule": "Host(`whoami.docker.localhost`)"})


def create_container(id, count):
    '''     change_directory = 'pwd'
        process1 = subprocess.Popen(change_directory.split(), stdout=subprocess.PIPE)
        print(process1.communicate()) '''
        
    command = 'docker-compose up -d'
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    return output


def create_container2(id, count):
    subprocess.call(['docker', 'scale', '--force', '{}={}'.format(id, count)])
    return client.containers.run(image, name=name, detach=True, labels={
        "traefik.http.routers.whoami.rule": "Host(`whoami.docker.localhost`)"})


def start_container(id):
    return client.containers.get(id).start()


def stop_container(id):
    return client.containers.get(id).stop()


def get_container_logs(id):
    return client.containers.get(id).logs()


async def get_container_list():
    return client.containers.list()


def get_container_by_id(id):
    return client.containers.get(id)


def get_container_by_name(name):
    return client.containers.get(name)


def remove_container(id):
    return client.containers.get(id).remove()


def remove_container_by_name(name):
    return client.containers.get(name).remove()


def remove_all_containers():
    return client.containers.prune()

# ***************** images *****************


def remove_all_images():
    return client.images.prune()


def get_image_list():
    return client.images.list()


def get_image_by_id(id):
    return client.images.get(id)


def get_image_by_name(name):
    return client.images.get(name)


def remove_image(id):
    return client.images.get(id).remove()


def remove_image_by_name(name):
    return client.images.get(name).remove()

# ***************** volumes *****************


def remove_all_volumes():
    return client.volumes.prune()


def get_volume_list():
    return client.volumes.list()


def get_volume_by_id(id):
    return client.volumes.get(id)


def get_volume_by_name(name):
    return client.volumes.get(name)


def remove_volume(id):
    return client.volumes.get(id).remove()


def remove_volume_by_name(name):
    return client.volumes.get(name).remove()

# ***************** networks *****************


def remove_all_networks():
    return client.networks.prune()


async def get_network_list():
    return client.networks.list()


def get_network_by_id(id):
    return client.networks.get(id)


def get_network_by_name(name):
    return client.networks.get(name)


def remove_network(id):
    return client.networks.get(id).remove()


def remove_network_by_name(name):
    return client.networks.get(name).remove()
