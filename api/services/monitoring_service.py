from fastapi import HTTPException
import json
from api.schemas.app import App
from api.clients import DockerClient
from sqlalchemy.orm import Session
from api.services.generator_service import docker_compose_generator, prometheus_yaml_generator, prometheus_scrape_generator, docker_compose_remove
import api.db.crud.app_crud as AppCrud
from typing import List
from api.config.constants import *


async def start_monitoring():
    try:
        # create network
        docker = await DockerClient.get_client(MONITORING_SERVICE_NAME)
        networks = docker.network.list()
        search = [network for network in networks if network.name ==
                  PROMETHEUS_NETWORK_NAME]
        if not search:
            docker.network.create(PROMETHEUS_NETWORK_NAME,
                                  driver=PROMETHEUS_NETWORK_DRIVER)
        docker.compose.up(detach=True)
        prometheus_yaml_generator()
        return {"message": "Monitoring started successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error starting monitoring. {e}")


async def stop_monitoring():
    try:
        docker = await DockerClient.get_client(MONITORING_SERVICE_NAME)
        docker.compose.stop()
        return {"message": "Monitoring stopped successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Error stopping monitoring. Please check if the monitoring service is running")


async def restart_monitoring():
    try:
        docker = await DockerClient.get_client(MONITORING_SERVICE_NAME)
        docker.compose.restart()
        return {"message": "Monitoring restarted successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error restarting monitoring. Please check if the monitoring service is running. ")
