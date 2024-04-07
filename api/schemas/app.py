''' This file contains the schema for the app model. '''
from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class App(BaseModel):
    id: Optional[int] = None
    name: str
    services: Optional[list]
    hosts: Optional[list] = None
    command: Optional[str] = None
    volumes: Optional[list] = None
    labels: Optional[list] = None
    min_scale: Optional[int] = None
    current_scale: Optional[int] = None
    max_scale: Optional[int] = None
    force_stop: Optional[bool] = None
    image: Optional[str] = None
    network: Optional[str] = None
    environment: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    user_id: Optional[int] = None


class AppDocker(App):
    docker: Optional[list] = None
    ip: Optional[str] = None
    ports: Optional[dict] = None
    status: Optional[str] = None


class ProxyRoute(BaseModel):
    ip: Optional[str] = None
    ports: Optional[dict] = None
    status: Optional[str] = None
