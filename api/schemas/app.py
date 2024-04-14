''' This file contains the schema for the app model. '''
from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class App(BaseModel):
    ''' This class defines the app schema '''
    id: Optional[int] = None
    name: str
    services: Optional[list] = None
    hosts: Optional[list] = None
    min_scale: Optional[int] = None
    current_scale: Optional[int] = None
    max_scale: Optional[int] = None
    force_stop: Optional[bool] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    user_id: Optional[int] = None


class Service(BaseModel):
    ''' This class defines the service schema contained in the app schema '''
    name: str
    image: str
    command: Optional[str] = None
    ports: Optional[list] = None
    volumes: Optional[list] = None
    networks: Optional[list] = None
    labels: Optional[list] = None


class AppDocker(App):
    ''' This class defines the app schema with docker dynamic fields '''
    docker: Optional[list] = None
    ip: Optional[str] = None
    ports: Optional[dict] = None
    status: Optional[str] = None


class ProxyRoute(BaseModel):
    ''' This class defines the proxy route schema '''
    ip: Optional[str] = None
    ports: Optional[dict] = None
    status: Optional[str] = None
