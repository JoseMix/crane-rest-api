import platform
import subprocess
import logging
from fastapi import FastAPI, HTTPException

app = FastAPI()


def is_docker_running():
    os_type = platform.system()

    if os_type == "Windows":
        # Windows: usamos `docker version` para verificarlo.
        try:
            output = subprocess.check_output(
                ["docker", "version"], stderr=subprocess.STDOUT
            ).decode()
            if "Server:" in output:
                return True
        except:
            pass

    elif os_type == "Darwin":
        # En MacOS, usamos `docker info` para verificarlo.
        try:
            subprocess.check_output("docker info", shell=True)
            return True
        except:
            pass

    else:
        # Asumiendo Linux u otro sistema operativo:
        try:
            # Si `docker info` ejecuta con éxito, Docker está corriendo.
            subprocess.check_output("docker info", shell=True)
            return True
        except:
            pass

    return False


def verify_docker_daemon():
    logger = logging.getLogger("api-log")

    if not is_docker_running():
        logger.error("Detectamos que Docker no está corriendo en este sistema")
        logger.error(
            "Por favor, inicie el servicio de Docker para que Crane funcione correctamente."
        )
        return False
    return True
    # Descomentar para mostrar el error en la API
    """ raise HTTPException(
        status_code=500, detail="Docker no está corriendo.") """
