import json
from typing import List
from fastapi import HTTPException
from api.schemas.app import App
from api.clients import DockerClient
from sqlalchemy.orm import Session
from api.services.generator_service import docker_compose_generator, docker_compose_remove
import api.db.crud.app_crud as AppCrud
from api.config.constants import RULES_SERVICE_NAME


async def start_rules():
    try:
        docker = await DockerClient.get_client(RULES_SERVICE_NAME)
        docker.compose.up(detach=True)
        return {"message": "Rules started successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error starting rules. {e}")


async def stop_rules():
    try:
        docker = await DockerClient.get_client(RULES_SERVICE_NAME)
        docker.compose.stop()
        return {"message": "Rules stopped successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Error stopping rules. Please check if the rules service is running")


async def restart_rules():
    try:
        docker = await DockerClient.get_client(RULES_SERVICE_NAME)
        docker.compose.restart()
        return {"message": "Rules restarted successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error restarting rules. Please check if the rules service is running. ")
