from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class App(BaseModel):
    id: Optional[int] = None
    name: str
    services: list
    ports: list = None
    hosts: list = None
    command: Optional[str] = None
    volumes: Optional[list] = None
    labels: Optional[list] = None
    scale: Optional[int] = None
    image: Optional[str] = None
    network: Optional[str] = None
    ip: Optional[str] = None
    port: Optional[str] = None
    count: Optional[int] = None
    environment: Optional[str] = None
    status: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    user_id: Optional[int] = None


class AppDocker(App):
    docker: Optional[dict] = None
